"""Unit and Integration Tests for Speech-First Frame Alignment and Voiceover Synchronization Engine.

Validates the Hybrid Two-Stage Speech-Lock Protocol:
- Snap-to-beat precision
- Zero cumulative drift across multiple shots
- Monotonic cue sequence constraints
- Frame conversion accuracy
- Offline fallback resilience
- Master audio buffer alignment
"""
import json
import math
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Safe Unicode output for Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from lib.audio.speech_sync import (
    SAMPLE_RATE,
    CHANNELS,
    SpeechSyncEngine,
    SpeechChunk,
    SpeechAlignmentResult,
)


class TestSpeechSyncEngine(unittest.TestCase):
    def setUp(self):
        self.bpm = 120.0
        self.fps = 30.0
        self.engine = SpeechSyncEngine(bpm=self.bpm, fps=self.fps, min_hold_s=0.5, beat_div=4)

    def test_beat_grid_parameters(self):
        # At 120 BPM: 60/120 = 0.5s per beat, 2.0s per bar (4 beats)
        self.assertAlmostEqual(self.engine.beat_len, 0.5, places=5)
        self.assertAlmostEqual(self.engine.bar_len, 2.0, places=5)

    def test_snap_to_grid(self):
        # Beat step = 2.0 / 4 = 0.5s
        # 1.1s should snap up to 1.5s in ceil mode
        self.assertAlmostEqual(self.engine.snap_to_grid(1.1, mode="ceil"), 1.5, places=4)
        # 1.0s should snap to 1.0s
        self.assertAlmostEqual(self.engine.snap_to_grid(1.0, mode="ceil"), 1.0, places=4)
        # 2.2s should snap to 2.5s
        self.assertAlmostEqual(self.engine.snap_to_grid(2.2, mode="ceil"), 2.5, places=4)
        # With beat_div=1 (full bars = 2.0s):
        bar_engine = SpeechSyncEngine(bpm=120.0, beat_div=1)
        self.assertAlmostEqual(bar_engine.snap_to_grid(2.1, mode="ceil"), 4.0, places=4)

    def test_frames_conversion_precision(self):
        self.assertEqual(self.engine.frames_from_seconds(0.0), 0)
        self.assertEqual(self.engine.frames_from_seconds(1.0), 30)
        self.assertEqual(self.engine.frames_from_seconds(2.5), 75)
        self.assertEqual(self.engine.frames_from_seconds(10.0), 300)
        self.assertAlmostEqual(self.engine.seconds_from_frames(75), 2.5, places=5)

    def test_offline_fallback_synthesis(self):
        text = "دانشگاه علوم پزشکی بقیه‌الله چهار سال صدرنشینی تحقیقات دانشجویی"
        audio, boundaries, dur = self.engine._synthesize_offline_fallback(text)
        self.assertGreater(dur, 1.0)
        self.assertEqual(audio.shape[1], CHANNELS)
        self.assertEqual(audio.shape[0], int(dur * SAMPLE_RATE))
        self.assertGreater(len(boundaries), 5)
        self.assertEqual(boundaries[0].text, "دانشگاه")

    def test_shotbook_alignment_zero_cumulative_drift(self):
        shots = [
            {
                "id": "shot_01_hook",
                "text": "در دل دانشگاه علوم پزشکی بقیه‌الله جریانی پویا در حرکت است",
                "min_hold_s": 0.5,
                "cues": {"punch": 0.5},
            },
            {
                "id": "shot_02_record",
                "text": "چهار سال صدرنشینی پنج ستاره در تحقیقات دانشجویی کشور",
                "min_hold_s": 0.6,
                "cues": {"badge": 0.4},
            },
            {
                "id": "shot_03_tech",
                "text": "رتبه نخست فناوری سلامت و کارآفرینی در سراسر دانشگاه‌ها",
                "min_hold_s": 0.5,
                "cues": {"award": 0.7},
            },
        ]

        # Use offline fallback for deterministic speed and network independence
        orig_synth = self.engine.synthesize_shot
        self.engine.synthesize_shot = self.engine._synthesize_offline_fallback

        try:
            result = self.engine.align_shotbook(shots)

            self.assertEqual(len(result.chunks), 3)
            self.assertGreater(result.total_seconds, 5.0)
            self.assertEqual(result.total_frames, int(round(result.total_seconds * 30.0)))

            # Verify zero cumulative drift: shot[i].start == shot[i-1].end
            for i in range(len(result.chunks)):
                chunk = result.chunks[i]
                if i > 0:
                    prev = result.chunks[i - 1]
                    self.assertEqual(
                        chunk.start_frame,
                        prev.end_frame,
                        f"Cumulative drift detected between {prev.shot_id} and {chunk.shot_id}!",
                    )
                    self.assertAlmostEqual(chunk.start_time_s, prev.end_time_s, places=4)

                # Verify monotonic ordering inside each shot:
                # start_frame <= speech_end_frame <= wipe_out <= end_frame
                self.assertLessEqual(chunk.start_frame, chunk.speech_end_frame)
                self.assertLessEqual(chunk.speech_end_frame, chunk.end_frame)

                # Verify breathing margin (shot end must be strictly after speech end)
                self.assertGreater(chunk.end_time_s, chunk.start_time_s + chunk.raw_duration_s)

            # Verify master audio dimensions
            expected_samples = int(math.ceil(result.total_seconds * SAMPLE_RATE))
            self.assertEqual(result.master_audio.shape, (expected_samples, CHANNELS))

            # Verify cues dictionary structure
            cues = result.cues_data
            self.assertTrue(cues["speech_aligned"])
            self.assertIn("shot_01_hook_start", cues["frames"])
            self.assertIn("shot_02_record_start", cues["frames"])
            self.assertIn("shot_03_tech_start", cues["frames"])
            self.assertEqual(cues["frames"]["shot_01_hook_start"], 0)

        finally:
            self.engine.synthesize_shot = orig_synth

    def test_save_and_reload_cues(self):
        shots = [
            {"id": "shot_01", "text": "آزمایش اول", "min_hold_s": 0.5},
            {"id": "shot_02", "text": "آزمایش دوم", "min_hold_s": 0.5},
        ]
        self.engine.synthesize_shot = self.engine._synthesize_offline_fallback

        with tempfile.TemporaryDirectory() as tmpdir:
            cues_path = Path(tmpdir) / "test_cues.json"
            wav_path = Path(tmpdir) / "master.wav"
            shots_dir = Path(tmpdir) / "shots"

            result = self.engine.align_shotbook(shots)
            result.save_cues(cues_path)
            result.save_master_audio(wav_path)
            shot_files = result.save_shot_audios(shots_dir)

            self.assertTrue(cues_path.exists())
            self.assertTrue(wav_path.exists())
            self.assertEqual(len(shot_files), 2)

            # Validate reloaded JSON
            with open(cues_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.assertEqual(loaded["bpm"], 120.0)
            self.assertEqual(len(loaded["shots"]), 2)
            self.assertIn("shot_01_start", loaded["frames"])


    def test_real_edge_tts_integration(self):
        # Smoke test live Edge-TTS synthesis (or graceful fallback)
        text = "پژوهش و فناوری"
        audio, boundaries, dur = self.engine.synthesize_shot(text)
        self.assertGreater(dur, 0.5)
        self.assertEqual(audio.shape[1], CHANNELS)
        self.assertEqual(len(audio), int(dur * SAMPLE_RATE))
        print(f"\n[LIVE TTS SMOKE] Text: '{text}' -> Dur: {dur:.2f}s, Boundaries: {len(boundaries)}")


if __name__ == "__main__":
    unittest.main()
