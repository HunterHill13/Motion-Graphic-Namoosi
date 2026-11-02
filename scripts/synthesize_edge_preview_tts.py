#!/usr/bin/env python3
"""
MICROSOFT EDGE-TTS PREVIEW SYNTHESIS ENGINE
=============================================
Role: Preview & Motion Validation Provider ONLY.
Never used as final production audio.
Zero Gemini quota consumption.

Features:
- Deterministic caching by script hash (audio/cache/edge_preview_tts/)
- Motion-only revision reuses cached audio with 0 TTS calls
- Master loudness normalization to EBU R128 (-16 LUFS)
- Output dedicated path: public/audio/preview/edge/{video_id}_preview_voice.wav
"""

import os
import sys
import asyncio
import hashlib
import wave
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import edge_tts
except ImportError:
    edge_tts = None

EDGE_DEFAULT_VOICE = "fa-IR-FaridNeural"
EDGE_FALLBACK_VOICE = "fa-IR-DilaraNeural"
EDGE_CACHE_DIR = Path("audio/cache/edge_preview_tts")


class EdgeTTSConfigurationError(Exception):
    pass


def compute_edge_cache_key(text: str, voice: str, rate: str = "+0%") -> str:
    script_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]
    sig = f"edge|{voice}|{rate}|{script_hash}"
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()[:32]


def measure_wav_duration(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return round(frames / float(rate), 2)


def normalize_to_ebu_r128(input_path: Path, output_wav_path: Path) -> bool:
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-af", "loudnorm=I=-16:TP=-1.0:LRA=7",
        "-ar", "44100",
        str(output_wav_path)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        output_wav_path.write_bytes(input_path.read_bytes())
        return False


async def _synthesize_edge_async(text: str, voice: str, temp_mp3: Path, rate: str = "+0%", pitch: str = "+0Hz"):
    if edge_tts is None:
        raise EdgeTTSConfigurationError("edge_tts package is not installed.")
    comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await comm.save(str(temp_mp3))


def synthesize_edge_preview(
    text: str,
    video_id: str = "preview_video",
    voice: str = EDGE_DEFAULT_VOICE,
    output_dir: Path = Path("public/audio/preview/edge"),
    rate: str = "+0%",
    pitch: str = "+0Hz",
    motion_only_revision: bool = False,
    mock_transport: Optional[Any] = None,
    force_fresh: bool = False,
    cache_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Synthesizes Preview narration with Microsoft Edge-TTS.
    Never consumes Gemini API quota.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    active_cache_dir = cache_dir or EDGE_CACHE_DIR
    active_cache_dir.mkdir(parents=True, exist_ok=True)

    cache_key = compute_edge_cache_key(text, voice, rate)
    cached_wav = active_cache_dir / f"{cache_key}.wav"
    dest_wav = output_dir / f"{video_id}_preview_voice.wav"

    # Motion-only revision or cache hit
    if not force_fresh and (motion_only_revision or cached_wav.exists()) and cached_wav.exists():
        dest_wav.write_bytes(cached_wav.read_bytes())
        duration = measure_wav_duration(dest_wav)
        return {
            "video_id": video_id,
            "provider": "edge-tts",
            "voice": voice,
            "duration": duration,
            "output_path": str(dest_wav),
            "cache_hit": True,
            "motion_only_reuse": motion_only_revision,
            "status": "SUCCESS"
        }

    # Live Edge-TTS synthesis
    temp_mp3 = output_dir / f"{video_id}_temp.mp3"

    if mock_transport is not None:
        # Hermetic testing hook: write mock 1s wav
        mock_transport(text, voice, dest_wav)
    else:
        asyncio.run(_synthesize_edge_async(text, voice, temp_mp3, rate, pitch))
        normalize_to_ebu_r128(temp_mp3, dest_wav)
        if temp_mp3.exists():
            temp_mp3.unlink()

    # Save to cache
    try:
        cached_wav.write_bytes(dest_wav.read_bytes())
    except Exception:
        pass

    duration = measure_wav_duration(dest_wav)

    return {
        "video_id": video_id,
        "provider": "edge-tts",
        "voice": voice,
        "duration": duration,
        "output_path": str(dest_wav),
        "cache_hit": False,
        "motion_only_reuse": False,
        "status": "SUCCESS"
    }


if __name__ == "__main__":
    print("Edge-TTS Preview Synthesis Engine Ready.")
    print(f"Default Preview Voice: {EDGE_DEFAULT_VOICE}")
