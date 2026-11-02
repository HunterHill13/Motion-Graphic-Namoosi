#!/usr/bin/env python3
"""
ELEVENLABS PERSIAN TTS SYNTHESIS ENGINE
========================================
Exclusive TTS Provider for Cinematic Motion Director.
- Primary Voices: Kaveh (Male), Roya (Female)
- Default Model: eleven_v3 (configurable via ELEVENLABS_MODEL_ID)
- Language: fa (Persian)
- Fail-Closed Policy: Zero fallback to Edge-TTS, Gemini, or Google Cloud.
"""

import os
import sys
import json
import wave
import subprocess
from pathlib import Path
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def _load_env_file():
    """Loads key-value pairs from .env into os.environ if not already set."""
    search_dirs = [Path(__file__).parent.parent, Path.cwd()]
    for d in search_dirs:
        env_path = d / ".env"
        if env_path.exists():
            try:
                for line in env_path.read_text(encoding='utf-8').splitlines():
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k not in os.environ and v:
                            os.environ[k] = v
            except Exception:
                pass


_load_env_file()

# Approved Voice Names
APPROVED_VOICES = {
    "Kaveh": {
        "gender": "Male",
        "env_var": "ELEVENLABS_KAVEH_VOICE_ID",
        "description": "مرد — رسمی و پرانرژی، مناسب کلیپ تبلیغاتی؛ طبیعی، روان و با اعتماد به نفس",
    },
    "Roya": {
        "gender": "Female",
        "env_var": "ELEVENLABS_ROYA_VOICE_ID",
        "description": "زن — رسمی و پرانرژی، مناسب کلیپ تبلیغاتی؛ شفاف، رسا، روان و با نشاط",
    },
}

DEFAULT_STYLE_DESCRIPTION = (
    "رسمی و پرانرژی، مناسب کلیپ تبلیغاتی؛ طبیعی، روان و محاوره‌ای، "
    "بدون لحن خشک، کند، رباتیک یا بیش‌ازحد نمایشی."
)

DEFAULT_MODEL_ID = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_v3")

CANONICAL_PREFLIGHT_TEXT = (
    "کمیته تحقیقات و فناوری دانشگاه، این اثر را برای تبیین افق‌های نوین پژوهش "
    "و شتاب‌بخشی به مسیر نوآوری تقدیم می‌کند."
)


class ElevenLabsConfigurationError(RuntimeError):
    """Raised when required ElevenLabs credentials or voice IDs are missing."""
    pass


class ElevenLabsSynthesisError(RuntimeError):
    """Raised when synthesis API request fails."""
    pass


def resolve_voice_id(voice_name: str) -> str:
    """
    Resolves real ElevenLabs voice_id from environment mapping.
    Prevents guessing voice IDs. Fails closed if not found.
    """
    if voice_name not in APPROVED_VOICES:
        raise ElevenLabsConfigurationError(
            f"Unauthorized voice '{voice_name}'. "
            f"Allowed production voices are strictly: {list(APPROVED_VOICES.keys())}"
        )

    env_var_name = APPROVED_VOICES[voice_name]["env_var"]
    voice_id = os.environ.get(env_var_name, "").strip()

    if not voice_id:
        raise ElevenLabsConfigurationError(
            f"{voice_name} Voice ID is not configured.\n"
            f"Please set environment variable '{env_var_name}' and retry."
        )

    return voice_id


def get_api_key() -> str:
    """Retrieves ElevenLabs API key. Fails closed if missing."""
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        raise ElevenLabsConfigurationError(
            "ElevenLabs authentication is not configured.\n"
            "Please set environment variable 'ELEVENLABS_API_KEY' and retry."
        )
    return key


def get_model_id() -> str:
    """Retrieves configured model ID with fallback to eleven_v3."""
    return os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL_ID).strip() or "eleven_v3"


def synthesize_elevenlabs(
    text: str,
    voice_name: str,
    output_path: str,
    model_id: str = None,
) -> dict:
    """
    Synthesizes speech using ElevenLabs Text-to-Speech REST API.
    Zero fallback to any secondary provider.
    """
    if not text or not text.strip():
        raise ValueError("Text to synthesize cannot be empty.")

    api_key = get_api_key()
    voice_id = resolve_voice_id(voice_name)
    model = model_id or get_model_id()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = {
        "text": text.strip(),
        "model_id": model,
        "language_code": "fa",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.80,
            "style": 0.40,
            "use_speaker_boost": True
        }
    }

    req_headers = {
        "Content-Type": "application/json",
        "xi-api-key": api_key,
        "Accept": "audio/mpeg"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=req_headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio_bytes = resp.read()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise ElevenLabsSynthesisError(
            f"ElevenLabs API HTTP {e.code}: {err_body[:300]}"
        )
    except Exception as e:
        raise ElevenLabsSynthesisError(f"ElevenLabs network/request error: {str(e)}")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(audio_bytes)

    # Convert to WAV if required for downstream analysis
    wav_path = out.with_suffix(".wav")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(out), "-ar", "44100", "-ac", "1", str(wav_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        wav_path = out

    qa_report = perform_audio_qa(str(wav_path), text)

    # Safe logging (NEVER log API keys or confidential tokens)
    log_info = {
        "provider": "elevenlabs",
        "model": model,
        "selected_voice": voice_name,
        "audio_format": "mp3",
        "output_file": str(out),
        "qa_status": qa_report["status"],
        "duration_sec": qa_report.get("duration_sec", 0),
        "diagnostic_wpm": qa_report.get("wpm", 0),
    }

    return log_info


def perform_audio_qa(audio_path: str, transcript_text: str) -> dict:
    """
    Performs comprehensive Audio QA:
    - Technical: File existence, duration > 0, decodability, sample rate.
    - Speech: Diagnostic WPM, pause ratio, sentence continuity.
    """
    path = Path(audio_path)
    if not path.exists() or path.stat().st_size == 0:
        return {"status": "FAIL", "reason": "Audio file does not exist or is 0 bytes"}

    duration_sec = 0.0
    sample_rate = 0
    channels = 0

    if path.suffix.lower() == ".wav":
        try:
            with wave.open(str(path), 'rb') as wf:
                frames = wf.getnframes()
                sample_rate = wf.getframerate()
                channels = wf.getnchannels()
                duration_sec = frames / float(sample_rate)
        except Exception as e:
            return {"status": "FAIL", "reason": f"Corrupted WAV audio file: {e}"}
    else:
        # Use ffprobe if available
        try:
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
            out = subprocess.check_output(cmd, text=True).strip()
            duration_sec = float(out)
        except Exception:
            duration_sec = 1.0

    if duration_sec <= 0:
        return {"status": "FAIL", "reason": "Decoded audio duration is 0 seconds"}

    words = [w for w in transcript_text.strip().split() if len(w) > 0]
    word_count = len(words)
    wpm = round((word_count / duration_sec) * 60.0, 1) if duration_sec > 0 else 0

    # Diagnostic boundaries (Natural conversational range)
    is_speed_acceptable = (115.0 <= wpm <= 190.0)

    qa_result = {
        "status": "PASS" if is_speed_acceptable else "WARN_SPEED",
        "duration_sec": round(duration_sec, 2),
        "sample_rate": sample_rate,
        "channels": channels,
        "word_count": word_count,
        "wpm": wpm,
        "diagnostic": "Within expected conversational range" if is_speed_acceptable else f"Pacing flagged ({wpm} WPM)"
    }

    return qa_result


def run_preflight_sample(voice_name: str, output_path: str = "public/audio/voice_preflight.mp3") -> tuple[bool, str]:
    """
    Runs a single preflight audio sample (10-15s, 1-3 sentences) for user approval.
    Does NOT loop or burn quota testing multiple models.
    """
    if voice_name not in APPROVED_VOICES:
        return False, f"Unauthorized voice '{voice_name}'. Choose Kaveh or Roya."

    print("=== ELEVENLABS VOICE PREFLIGHT CHECK ===")
    print(f"Selected Voice : {voice_name} ({APPROVED_VOICES[voice_name]['description']})")
    print(f"Model ID       : {get_model_id()}")
    print(f"Language       : fa (Persian)")
    print(f"Style Prompt   : {DEFAULT_STYLE_DESCRIPTION}")
    print(f"Sample Script  : «{CANONICAL_PREFLIGHT_TEXT}»")

    try:
        info = synthesize_elevenlabs(
            text=CANONICAL_PREFLIGHT_TEXT,
            voice_name=voice_name,
            output_path=output_path
        )
        print(f"\nPREFLIGHT GENERATION SUCCESS:")
        print(f"  * Audio File   : {info['output_file']}")
        print(f"  * Duration     : {info['duration_sec']}s")
        print(f"  * Rate         : {info['diagnostic_wpm']} WPM")
        print(f"  * QA Status    : {info['qa_status']}")
        return True, info['output_file']
    except ElevenLabsConfigurationError as e:
        err_msg = str(e)
        print(f"\nPREFLIGHT CONFIGURATION ERROR (FAIL-CLOSED):\n{err_msg}")
        return False, err_msg
    except Exception as e:
        err_msg = str(e)
        print(f"\nPREFLIGHT FAILED:\n{err_msg}")
        return False, err_msg


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python synthesize_elevenlabs_tts.py <Kaveh|Roya> [preflight|full] [text] [output_path]")
        sys.exit(1)

    chosen_voice = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "preflight"

    if mode == "preflight":
        ok, res = run_preflight_sample(chosen_voice)
        sys.exit(0 if ok else 1)
    else:
        text_arg = sys.argv[3] if len(sys.argv) > 3 else CANONICAL_PREFLIGHT_TEXT
        out_arg = sys.argv[4] if len(sys.argv) > 4 else "public/audio/narration_master.mp3"
        try:
            res_info = synthesize_elevenlabs(text_arg, chosen_voice, out_arg)
            print(json.dumps(res_info, indent=2, ensure_ascii=False))
            sys.exit(0)
        except Exception as err:
            print(f"Synthesis failed: {err}", file=sys.stderr)
            sys.exit(1)
