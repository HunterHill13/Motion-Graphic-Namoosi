"""Speech-First Frame Alignment and Voiceover Synchronization Engine.

Implements the Hybrid Two-Stage Speech-Lock Protocol:
1. Per-shot neural voice synthesis (Edge-TTS or offline fallback).
2. Word & sentence boundary extraction (100ns precision).
3. Musical beat & bar grid snapping (snapToBeat).
4. Direct calculation of frame-accurate cue sheets (cues.json).
5. Assembly of zero-drift master voiceover track (48kHz stereo).

Prevents dual-truth discrepancies, monolithic audio dumping, and cumulative drift.
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import soundfile as sf

# 48kHz stereo standard for mgaudio and production pipeline
SAMPLE_RATE = 48000
CHANNELS = 2


@dataclass
class BoundaryEvent:
    text: str
    offset_s: float
    duration_s: float
    end_s: float

    @property
    def offset_100ns(self) -> int:
        return int(self.offset_s * 10_000_000)


@dataclass
class SpeechChunk:
    shot_id: str
    text: str
    raw_audio: np.ndarray
    raw_duration_s: float
    boundaries: List[BoundaryEvent]
    start_time_s: float = 0.0
    end_time_s: float = 0.0
    start_frame: int = 0
    end_frame: int = 0
    speech_end_frame: int = 0
    internal_cues: Dict[str, int] = field(default_factory=dict)
    audio_filename: Optional[str] = None


@dataclass
class SpeechAlignmentResult:
    bpm: float
    fps: float
    total_seconds: float
    total_frames: int
    chunks: List[SpeechChunk]
    cues_data: Dict[str, Any]
    master_audio: np.ndarray

    def save_cues(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.cues_data, f, indent=2, ensure_ascii=False)

    def save_master_audio(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(p), self.master_audio, SAMPLE_RATE, subtype="FLOAT")

    def save_shot_audios(self, dir_path: str | Path) -> List[str]:
        dp = Path(dir_path)
        dp.mkdir(parents=True, exist_ok=True)
        out_paths = []
        for chunk in self.chunks:
            fname = chunk.audio_filename or f"{chunk.shot_id}_vox.wav"
            fpath = dp / fname
            sf.write(str(fpath), chunk.raw_audio, SAMPLE_RATE, subtype="FLOAT")
            out_paths.append(str(fpath))
        return out_paths


class SpeechSyncEngine:
    def __init__(
        self,
        bpm: float = 120.0,
        fps: float = 30.0,
        voice: str = "fa-IR-FaridNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        min_hold_s: float = 0.5,
        beat_div: int = 4,  # 4 = snap to quarter notes / beats (0.5s at 120 BPM in 4/4)
        lead_in_s: float = 0.0,
    ):
        self.bpm = float(bpm)
        self.fps = float(fps)
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.min_hold_s = float(min_hold_s)
        self.beat_div = int(beat_div)
        self.lead_in_s = float(lead_in_s)

    @property
    def beat_len(self) -> float:
        return 60.0 / self.bpm

    @property
    def bar_len(self) -> float:
        return self.beat_len * 4.0

    def snap_to_grid(self, t: float, mode: str = "ceil") -> float:
        """Snap a duration or time to the musical beat grid.
        div=4 means snapping to quarter notes (every beat).
        div=2 means snapping to half notes.
        div=1 means snapping to full 4-beat bars.
        """
        step = self.bar_len / self.beat_div
        k = t / step
        if mode == "ceil":
            k_snapped = math.ceil(k - 1e-9)
        elif mode == "floor":
            k_snapped = math.floor(k + 1e-9)
        else:
            k_snapped = round(k)
        return max(step, k_snapped * step)

    def frames_from_seconds(self, s: float) -> int:
        return int(round(s * self.fps))

    def seconds_from_frames(self, f: int) -> float:
        return float(f) / self.fps

    async def _synthesize_edge_tts(self, text: str, voice: Optional[str] = None) -> Tuple[np.ndarray, List[BoundaryEvent], float]:
        """Synthesize text using edge-tts, returning 48kHz stereo float32 and boundary events."""
        import edge_tts

        selected_voice = voice or self.voice
        comm = edge_tts.Communicate(text, selected_voice, rate=self.rate, volume=self.volume)
        mp3_buffer = bytearray()
        boundaries: List[BoundaryEvent] = []

        async for chunk in comm.stream():
            ctype = chunk.get("type")
            if ctype == "audio":
                mp3_buffer.extend(chunk["data"])
            elif ctype in ("WordBoundary", "SentenceBoundary"):
                # offset and duration in 100ns units (10,000,000 units = 1s)
                off_s = chunk.get("offset", 0) / 10_000_000.0
                dur_s = chunk.get("duration", 0) / 10_000_000.0
                txt = chunk.get("text", "")
                boundaries.append(BoundaryEvent(text=txt, offset_s=off_s, duration_s=dur_s, end_s=off_s + dur_s))

        if not mp3_buffer:
            raise RuntimeError("Edge-TTS returned empty audio stream.")

        # Decode MP3 to 48kHz stereo WAV via ffmpeg
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            "pipe:0",
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            str(CHANNELS),
            "-f",
            "wav",
            "pipe:1",
        ]
        res = subprocess.run(
            cmd,
            input=bytes(mp3_buffer),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        audio, sr = sf.read(io.BytesIO(res.stdout), dtype="float32")
        if audio.ndim == 1:
            audio = np.column_stack((audio, audio))
        dur_s = len(audio) / SAMPLE_RATE

        return audio, boundaries, dur_s

    def _synthesize_offline_fallback(self, text: str, voice: Optional[str] = None) -> Tuple[np.ndarray, List[BoundaryEvent], float]:
        """Procedural tone/envelope fallback for airgapped or offline testing.
        Calculates realistic duration based on Persian word count (~2.8 words/sec).
        """
        words = [w for w in re.split(r"\s+", text.strip()) if w]
        word_count = max(1, len(words))
        # Estimate duration: average 0.35s per Persian word + 0.3s breath
        est_dur = max(1.2, word_count * 0.35 + 0.3)
        total_samples = int(est_dur * SAMPLE_RATE)

        # Generate a warm low-frequency voice-like tone envelope (fundamental 130 Hz)
        t = np.linspace(0, est_dur, total_samples, endpoint=False)
        sine = 0.15 * np.sin(2 * np.pi * 130 * t) + 0.08 * np.sin(2 * np.pi * 260 * t)
        # Apply smooth attack & release
        env = np.ones(total_samples, dtype=np.float32)
        att = min(int(0.05 * SAMPLE_RATE), total_samples // 4)
        rel = min(int(0.10 * SAMPLE_RATE), total_samples // 4)
        env[:att] = np.linspace(0, 1, att)
        env[-rel:] = np.linspace(1, 0, rel)
        mono = (sine * env).astype(np.float32)
        stereo = np.column_stack((mono, mono))

        # Synthetic boundaries per word
        boundaries = []
        w_dur = (est_dur - 0.2) / word_count
        for i, w in enumerate(words):
            off = 0.1 + i * w_dur
            boundaries.append(BoundaryEvent(text=w, offset_s=off, duration_s=w_dur * 0.85, end_s=off + w_dur * 0.85))

        return stereo, boundaries, est_dur

    def synthesize_shot(self, text: str, voice: Optional[str] = None) -> Tuple[np.ndarray, List[BoundaryEvent], float]:
        """Synthesizes voice with automatic fallback to offline procedural simulation if network fails."""
        if not text or not text.strip():
            # 0.5s silence for empty narration
            silence = np.zeros((int(0.5 * SAMPLE_RATE), CHANNELS), dtype=np.float32)
            return silence, [], 0.5

        try:
            return asyncio.run(self._synthesize_edge_tts(text, voice))
        except Exception as e:
            sys.stderr.write(f"[WARN] Edge-TTS synthesis failed ({e}). Using offline acoustic fallback.\n")
            return self._synthesize_offline_fallback(text)

    def align_shotbook(
        self,
        shots: List[Dict[str, Any]],
        existing_cues: Optional[Dict[str, Any]] = None,
        voice: Optional[str] = None,
    ) -> SpeechAlignmentResult:
        """Processes a list of shot specifications and builds a zero-drift frame-locked cue sheet.

        Each shot spec dict can contain:
        - id: str (e.g. "shot_01_hook")
        - text: str (narration line)
        - min_hold_s: float (extra visual hold after speech finishes, default self.min_hold_s)
        - internal_cues: dict (e.g. {"photo_reveal": "offset_s" or relative float 0..1})
        """
        accum_time_s = 0.0
        chunks: List[SpeechChunk] = []

        all_frames: Dict[str, int] = {}
        if existing_cues and "frames" in existing_cues:
            all_frames.update(existing_cues["frames"])

        for i, s in enumerate(shots):
            shot_id = s.get("id", f"shot_{i+1:02d}")
            text = s.get("text", "")
            hold_s = float(s.get("min_hold_s", self.min_hold_s))

            # 1. Synthesize audio
            audio, boundaries, dur_s = self.synthesize_shot(text, voice=voice)

            # 2. Target shot duration = speech duration + hold margin
            raw_target_dur = dur_s + hold_s

            # 3. Snap duration to musical beat grid
            snapped_shot_dur = self.snap_to_grid(raw_target_dur, mode="ceil")

            # 4. Compute timeline bounds
            start_s = accum_time_s
            end_s = start_s + snapped_shot_dur
            speech_end_s = start_s + dur_s

            start_f = self.frames_from_seconds(start_s)
            end_f = self.frames_from_seconds(end_s)
            speech_end_f = self.frames_from_seconds(speech_end_s)

            # 5. Compute internal cues
            cues_map: Dict[str, int] = {
                f"{shot_id}_start": start_f,
                f"{shot_id}_speech_end": speech_end_f,
                f"{shot_id}_wipe_out": max(start_f, end_f - self.frames_from_seconds(0.4)),
                f"{shot_id}_end": end_f,
            }

            # Map user-specified internal cues (either word matches or relative times)
            custom_cues = s.get("cues", {})
            for c_name, c_val in custom_cues.items():
                if isinstance(c_val, (int, float)):
                    # If 0.0 <= c_val <= 1.0, treat as fraction of speech duration
                    if 0.0 <= c_val <= 1.0:
                        cue_t = start_s + c_val * dur_s
                    else:
                        cue_t = start_s + float(c_val)
                    cues_map[f"{shot_id}_{c_name}"] = self.frames_from_seconds(cue_t)
                elif isinstance(c_val, str):
                    # Try matching a word in boundaries
                    matched = False
                    for b in boundaries:
                        if c_val in b.text:
                            cues_map[f"{shot_id}_{c_name}"] = self.frames_from_seconds(start_s + b.offset_s)
                            matched = True
                            break
                    if not matched:
                        # Default to middle of speech
                        cues_map[f"{shot_id}_{c_name}"] = self.frames_from_seconds(start_s + dur_s * 0.5)

            chunk = SpeechChunk(
                shot_id=shot_id,
                text=text,
                raw_audio=audio,
                raw_duration_s=dur_s,
                boundaries=boundaries,
                start_time_s=start_s,
                end_time_s=end_s,
                start_frame=start_f,
                end_frame=end_f,
                speech_end_frame=speech_end_f,
                internal_cues=cues_map,
                audio_filename=f"{shot_id}_vox.wav",
            )
            chunks.append(chunk)
            all_frames.update(cues_map)

            # Advance cumulative time
            accum_time_s = end_s

        total_seconds = accum_time_s
        total_frames = self.frames_from_seconds(total_seconds)

        # 6. Assemble zero-drift master voiceover track
        total_samples = int(math.ceil(total_seconds * SAMPLE_RATE))
        master_audio = np.zeros((total_samples, CHANNELS), dtype=np.float32)

        for chunk in chunks:
            start_sample = int(chunk.start_time_s * SAMPLE_RATE)
            chunk_len = len(chunk.raw_audio)
            end_sample = min(total_samples, start_sample + chunk_len)
            copy_len = end_sample - start_sample
            if copy_len > 0:
                master_audio[start_sample:end_sample] += chunk.raw_audio[:copy_len]

        # 7. Formulate cues.json dictionary
        cues_data: Dict[str, Any] = {
            "bpm": self.bpm,
            "fps": self.fps,
            "total_seconds": round(total_seconds, 3),
            "total_frames": total_frames,
            "speech_aligned": True,
            "voice": self.voice,
            "shots": [
                {
                    "id": c.shot_id,
                    "text": c.text,
                    "start_time": round(c.start_time_s, 3),
                    "end_time": round(c.end_time_s, 3),
                    "duration": round(c.end_time_s - c.start_time_s, 3),
                    "speech_duration": round(c.raw_duration_s, 3),
                    "start_frame": c.start_frame,
                    "end_frame": c.end_frame,
                    "speech_end_frame": c.speech_end_frame,
                    "audio_file": c.audio_filename,
                    "boundaries": [
                        {
                            "text": b.text,
                            "offset": round(b.offset_s, 3),
                            "duration": round(b.duration_s, 3),
                        }
                        for b in c.boundaries
                    ],
                }
                for c in chunks
            ],
            "frames": all_frames,
        }

        return SpeechAlignmentResult(
            bpm=self.bpm,
            fps=self.fps,
            total_seconds=total_seconds,
            total_frames=total_frames,
            chunks=chunks,
            cues_data=cues_data,
            master_audio=master_audio,
        )


def main():
    parser = argparse.ArgumentParser(description="Speech-First Frame Alignment and Voiceover Engine")
    parser.add_argument("--shotbook", type=str, required=True, help="Path to JSON file containing list of shots")
    parser.add_argument("--out-cues", type=str, default="cues.json", help="Output path for synced cues.json")
    parser.add_argument("--out-audio-dir", type=str, default="public/audio", help="Directory to save WAV files")
    parser.add_argument("--out-master-audio", type=str, default="public/audio/master_voiceover.wav", help="Path for assembled master voiceover")
    parser.add_argument("--bpm", type=float, default=120.0, help="Music tempo (BPM)")
    parser.add_argument("--fps", type=float, default=30.0, help="Animation framerate")
    parser.add_argument("--voice", type=str, default="fa-IR-FaridNeural", help="Edge-TTS voice")
    parser.add_argument("--min-hold", type=float, default=0.5, help="Minimum hold margin after speech (seconds)")
    parser.add_argument("--beat-div", type=int, default=4, help="Grid snapping division per bar (4=quarter notes/beats, 1=bars)")

    args = parser.parse_args()

    with open(args.shotbook, "r", encoding="utf-8") as f:
        shots_data = json.load(f)

    if isinstance(shots_data, dict) and "shots" in shots_data:
        shots_list = shots_data["shots"]
    elif isinstance(shots_data, list):
        shots_list = shots_data
    else:
        raise ValueError("Shotbook JSON must be a list of shots or an object with 'shots' key.")

    engine = SpeechSyncEngine(
        bpm=args.bpm,
        fps=args.fps,
        voice=args.voice,
        min_hold_s=args.min_hold,
        beat_div=args.beat_div,
    )

    print(f"Aligning {len(shots_list)} shots at {args.bpm} BPM / {args.fps} FPS with voice '{args.voice}'...")
    result = engine.align_shotbook(shots_list, voice=args.voice)

    result.save_cues(args.out_cues)
    print(f"[OK] Saved synced cue sheet to: {args.out_cues} ({result.total_frames} frames, {result.total_seconds:.2f}s)")

    if args.out_audio_dir:
        saved_files = result.save_shot_audios(args.out_audio_dir)
        print(f"[OK] Saved {len(saved_files)} shot WAVs to: {args.out_audio_dir}")

    if args.out_master_audio:
        result.save_master_audio(args.out_master_audio)
        print(f"[OK] Saved master voiceover track to: {args.out_master_audio}")


if __name__ == "__main__":
    main()
