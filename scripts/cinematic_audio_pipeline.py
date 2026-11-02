#!/usr/bin/env python3
"""
CINEMATIC AUDIO PIPELINE & APPROVAL STATE MACHINE
===================================================
Orchestrates the two-stage TTS architecture:
Stage 1: Microsoft Edge-TTS Preview for complete Motion Graphics validation (Zero Gemini quota)
Stage 2: Quota-Aware Google Gemini TTS Final Production (Only upon explicit user approval)

State Machine:
  DRAFT
    ↓
  EDGE_PREVIEW_GENERATING
    ↓
  EDGE_PREVIEW_READY
    ↓
  WAITING_USER_APPROVAL
    ├── REVISION  ──► EDGE_PREVIEW_GENERATING (re-renders motion, reuses Edge audio if script unchanged)
    ├── CANCEL    ──► CANCELLED
    └── APPROVE   ──► GEMINI_PREFLIGHT
                          ↓
                      GEMINI_VOICE_APPROVAL
                          ↓
                      GEMINI_FINAL_GENERATION
                          ↓
                      FINAL_TIMING_CALIBRATION (Gemini actual duration = Source of Truth)
                          ↓
                      FINAL_RENDER
                          ↓
                      DONE
"""

import os
import sys
import json
import wave
from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum

from scripts.synthesize_edge_preview_tts import synthesize_edge_preview, measure_wav_duration
from scripts.synthesize_gemini_tts import (
    synthesize_narration,
    run_preflight_sample,
    MODEL_PRIORITY,
    ALLOWED_VOICES as GEMINI_ALLOWED_VOICES,
    GeminiTTSQuotaError,
    GeminiTTSConfigurationError
)


class PipelineState(str, Enum):
    DRAFT = "DRAFT"
    EDGE_PREVIEW_GENERATING = "EDGE_PREVIEW_GENERATING"
    EDGE_PREVIEW_READY = "EDGE_PREVIEW_READY"
    WAITING_USER_APPROVAL = "WAITING_USER_APPROVAL"
    REVISION = "REVISION"
    CANCELLED = "CANCELLED"
    GEMINI_PREFLIGHT = "GEMINI_PREFLIGHT"
    GEMINI_VOICE_APPROVAL = "GEMINI_VOICE_APPROVAL"
    GEMINI_FINAL_GENERATION = "GEMINI_FINAL_GENERATION"
    FINAL_TIMING_CALIBRATION = "FINAL_TIMING_CALIBRATION"
    FINAL_RENDER = "FINAL_RENDER"
    DONE = "DONE"


class PipelineApprovalError(Exception):
    """Raised when an attempt is made to call Gemini without explicit user approval."""
    pass


class CinematicAudioPipeline:
    def __init__(
        self,
        video_id: str,
        script_text: str,
        gemini_voice: str = "Puck",
        edge_voice: Optional[str] = None,
        fps: int = 30
    ):
        self.video_id = video_id
        self.script_text = script_text.strip()
        self.gemini_voice = gemini_voice
        self.edge_voice = edge_voice if edge_voice else ("fa-IR-DilaraNeural" if gemini_voice == "Callirrhoe" else "fa-IR-FaridNeural")
        self.fps = fps

        self.state = PipelineState.DRAFT
        self.user_approved_preview = False
        self.user_approved_gemini_voice = False

        # Accounting and Artefacts
        self.edge_preview_audio_path: Optional[str] = None
        self.edge_preview_duration: float = 0.0
        self.gemini_final_audio_path: Optional[str] = None
        self.gemini_final_duration: float = 0.0

        self.preview_render_path: Optional[str] = None
        self.final_render_path: Optional[str] = None

        self.gemini_requests_sent = 0
        self.edge_requests_sent = 0
        self.timing_map: Dict[str, Any] = {}

    def generate_edge_preview(
        self,
        motion_only_revision: bool = False,
        output_dir: Path = Path("public/audio/preview/edge"),
        mock_transport: Optional[Any] = None,
        force_fresh: bool = False,
        cache_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Generates full Edge-TTS preview audio for motion validation.
        GUARANTEE: ZERO GEMINI REQUESTS. ZERO GEMINI QUOTA.
        """
        self.state = PipelineState.EDGE_PREVIEW_GENERATING

        res = synthesize_edge_preview(
            text=self.script_text,
            video_id=self.video_id,
            voice=self.edge_voice,
            output_dir=output_dir,
            motion_only_revision=motion_only_revision,
            mock_transport=mock_transport,
            force_fresh=force_fresh,
            cache_dir=cache_dir
        )

        self.edge_preview_audio_path = res["output_path"]
        self.edge_preview_duration = res["duration"]
        if not res["cache_hit"] and not res["motion_only_reuse"]:
            self.edge_requests_sent += 1

        # Derive provisional timing for preview render
        preview_total_frames = int(self.edge_preview_duration * self.fps)
        self.preview_render_path = f"renders/preview/{self.video_id}_preview_edge.mp4"

        self.timing_map = {
            "source": "edge-tts",
            "duration_sec": self.edge_preview_duration,
            "total_frames": preview_total_frames,
            "fps": self.fps,
            "is_final": False
        }

        self.state = PipelineState.EDGE_PREVIEW_READY
        self.state = PipelineState.WAITING_USER_APPROVAL

        return {
            "video_id": self.video_id,
            "state": self.state.value,
            "edge_audio_path": self.edge_preview_audio_path,
            "preview_duration": self.edge_preview_duration,
            "preview_render_path": self.preview_render_path,
            "gemini_requests_sent": self.gemini_requests_sent,
            "cache_hit": res["cache_hit"],
            "motion_only_reuse": res["motion_only_reuse"],
            "message": (
                "🎬 Preview با Microsoft Edge-TTS آماده شد. "
                "این نسخه برای بررسی ریتم، موشن، ترنزیشن‌ها و کامپوزیشن است. "
                "هنوز هیچ سهمیه Gemini مصرف نشده است. منتظر تأیید کاربر..."
            )
        }

    def submit_user_review(
        self,
        decision: str,
        feedback: Optional[str] = None,
        new_script: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes the user's review of the Edge-TTS Preview:
        - APPROVE: Unlocks the Gemini Final production gate.
        - REVISION: Returns to preview stage. If script unchanged, reuses audio.
        - CANCEL: Cancels the pipeline.
        """
        decision_clean = decision.strip().lower()
        approve_keywords = ["approve", "approved", "تأیید", "تایید", "اوکی", "برو برای gemini", "yes", "بله"]

        if any(k in decision_clean for k in approve_keywords):
            self.user_approved_preview = True
            self.state = PipelineState.GEMINI_PREFLIGHT
            return {
                "decision": "APPROVE",
                "state": self.state.value,
                "message": "پیش‌نمایش موشن گرافیک تأیید شد. خط لوله تولید نهایی Gemini باز شد."
            }

        cancel_keywords = ["cancel", "لغو", "انصراف", "stop", "متوقف"]
        if any(k in decision_clean for k in cancel_keywords):
            self.state = PipelineState.CANCELLED
            return {
                "decision": "CANCEL",
                "state": self.state.value,
                "message": "تولید توسط کاربر لغو شد."
            }

        # Otherwise treat as REVISION
        self.state = PipelineState.REVISION
        script_changed = False
        if new_script and new_script.strip() != self.script_text:
            self.script_text = new_script.strip()
            script_changed = True

        return {
            "decision": "REVISION",
            "state": self.state.value,
            "script_changed": script_changed,
            "feedback": feedback,
            "message": "بازخورد اصلاحی ثبت شد. بازگشت به فاز Preview بدون مصرف کووتای Gemini."
        }

    def execute_gemini_final(
        self,
        output_dir: Path = Path("public/audio/final/gemini"),
        mock_gemini_transport: Optional[Any] = None,
        force_fresh: bool = False
    ) -> Dict[str, Any]:
        """
        Executes Gemini Final Production.
        STRICT SECURITY GATE: Refuses to run if user has not explicitly approved the Preview.
        """
        if not self.user_approved_preview:
            raise PipelineApprovalError(
                "CRITICAL VIOLATION: Gemini TTS execution is strictly prohibited before explicit user approval of the Edge-TTS Preview."
            )

        # 1. Gemini Voice Approval Gate
        self.state = PipelineState.GEMINI_VOICE_APPROVAL

        # 2. Gemini Final Generation (Monolithic single-request)
        self.state = PipelineState.GEMINI_FINAL_GENERATION

        gemini_res = synthesize_narration(
            text=self.script_text,
            voice=self.gemini_voice,
            video_id=self.video_id,
            output_dir=output_dir,
            transport=mock_gemini_transport,
            force_fresh=force_fresh
        )

        self.gemini_requests_sent += gemini_res["request_count"]
        self.gemini_final_audio_path = gemini_res["output_path"]
        self.gemini_final_duration = gemini_res["audio_duration"]

        # 3. Final Timing Recalibration
        self.state = PipelineState.FINAL_TIMING_CALIBRATION
        final_total_frames = int(self.gemini_final_duration * self.fps)
        duration_delta = round(self.gemini_final_duration - self.edge_preview_duration, 2)

        self.timing_map = {
            "source": f"gemini ({gemini_res['actual_model']})",
            "duration_sec": self.gemini_final_duration,
            "total_frames": final_total_frames,
            "fps": self.fps,
            "edge_preview_duration_sec": self.edge_preview_duration,
            "duration_delta_sec": duration_delta,
            "is_final": True
        }

        # 4. Final Render Path
        self.state = PipelineState.FINAL_RENDER
        self.final_render_path = f"renders/final/{self.video_id}_final_gemini.mp4"
        self.state = PipelineState.DONE

        return {
            "video_id": self.video_id,
            "state": self.state.value,
            "actual_model": gemini_res["actual_model"],
            "fallback_used": gemini_res["fallback_used"],
            "fallback_reason": gemini_res["fallback_reason"],
            "gemini_final_audio_path": self.gemini_final_audio_path,
            "gemini_final_duration": self.gemini_final_duration,
            "edge_preview_duration": self.edge_preview_duration,
            "duration_delta": duration_delta,
            "timing_map": self.timing_map,
            "final_render_path": self.final_render_path,
            "gemini_requests_sent": self.gemini_requests_sent,
            "status": "SUCCESS"
        }
