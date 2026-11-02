#!/usr/bin/env python3
"""
QUOTA-AWARE GEMINI TTS SYNTHESIS ENGINE
=========================================
Architectural Specification:
- Primary Model: gemini-3.8-flash-tts (Priority 1 - Default)
- Fallback 1: gemini-3.8-flash-lite-tts (Priority 2 - Quota/Rate-limit only)
- Fallback 2: gemini-3.1-flash-tts-preview (Priority 3 - Quota/Rate-limit legacy fallback)
- Voices:
    - Male: Puck (رسمی، پرانرژی، مدرن و پویا)
    - Female: Callirrhoe (طبیعی، آرام، صمیمی و روان)
- Single Video = One TTS Request (Monolithic generation)
- Fail-closed security: Never leaks GEMINI_API_KEY in logs/reports
- Zero-probing doctrine: Never probes models to "test" connectivity
- Deterministic Disk Caching
"""

import os
import sys
import json
import base64
import wave
import hashlib
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
import urllib.request
import urllib.error

# Official Model Priority Hierarchy
MODEL_PRIORITY: List[str] = [
    "gemini-3.8-flash-tts",          # Priority 1: Default / Highest Quality
    "gemini-3.8-flash-lite-tts",     # Priority 2: First Quota Fallback
    "gemini-3.1-flash-tts-preview"   # Priority 3: Final Legacy Quota Fallback
]

ALLOWED_VOICES: Dict[str, Dict[str, str]] = {
    "Puck": {
        "gender": "Male",
        "character": "Upbeat",
        "desc": "رسمی، پرانرژی، مدرن و پویا (مناسب کلیپ‌های علمی، تبلیغاتی و سینمایی)"
    },
    "Callirrhoe": {
        "gender": "Female",
        "character": "Easy-going",
        "desc": "طبیعی، آرام، صمیمی و روان (مناسب محتوای آموزشی و توضیحی فاخر)"
    }
}

DEFAULT_STYLE_INSTRUCTION = (
    "رسمی و پرانرژی، مناسب کلیپ تبلیغاتی؛ "
    "طبیعی، روان و محاوره‌ای، با ریتم مناسب و confident delivery، "
    "بدون لحن گویندگی خشک، رسمیِ سنگین یا اغراق‌آمیز."
)

DEFAULT_LANGUAGE = "fa-IR"
CANONICAL_PREFLIGHT_TEXT = (
    "کمیته تحقیقات دانشگاه علوم پزشکی بقیه‌الله، این ویدیو را برای معرفی مسیر جدید پژوهش و نوآوری تقدیم می‌کند."
)

CACHE_DIR = Path("audio/cache/gemini_tts")


class GeminiTTSQuotaError(Exception):
    """Raised when all available Gemini TTS models hit quota or rate limits."""
    pass


class GeminiTTSConfigurationError(Exception):
    """Raised when configuration, voice, or authentication credentials are invalid."""
    pass


class GeminiTTSNonQuotaError(Exception):
    """Raised when an API error occurs that is NOT related to quota/rate-limit."""
    pass


def is_authentic_quota_failure(status_code: int, response_text: str) -> bool:
    """
    Determines with mechanical certainty if an error is an authentic quota or rate limit exhaustion.
    Only authentic quota exhaustion may trigger fallback.
    """
    if status_code == 429:
        return True

    quota_signatures = [
        "RESOURCE_EXHAUSTED",
        "quota exceeded",
        "rate limit",
        "GenerateRequestsPerDayPerProjectPerModel-FreeTier",
        "generativelanguage.googleapis.com/generate_content_free_tier_requests",
        "generativelanguage.googleapis.com/generate_content_free_tier_input_token_count",
        "daily request limit",
        "per-project per-model quota",
        "QuotaFailure",
        "RateLimitExceeded"
    ]

    lower_resp = response_text.lower()
    for sig in quota_signatures:
        if sig.lower() in lower_resp:
            return True

    return False


def get_sanitized_api_key() -> str:
    """Retrieves GEMINI_API_KEY from environment, failing closed if missing."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key or not key.strip():
        raise GeminiTTSConfigurationError(
            "GEMINI_API_KEY is not set in environment. "
            "Please configure GEMINI_API_KEY in your environment before generating narration."
        )
    return key.strip()


def compute_cache_key(model: str, voice: str, language: str, text: str, style: str) -> str:
    """Computes a deterministic SHA256 cache key."""
    script_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]
    style_hash = hashlib.sha256(style.strip().encode("utf-8")).hexdigest()[:16]
    sig = f"gemini|{model}|{voice}|{language}|{script_hash}|{style_hash}"
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()[:32]


def build_gemini_payload(text: str, voice: str, style_prompt: str = "") -> Dict[str, Any]:
    """Constructs the standard Generative Language API payload for audio synthesis."""
    # TTS models read content text verbatim; do not inject instructions into spoken content
    clean_text = text.strip()
    return {
        "contents": [
            {
                "parts": [
                    {"text": clean_text}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice
                    }
                }
            }
        }
    }


def send_gemini_request(
    model: str,
    payload: Dict[str, Any],
    api_key: str,
    transport: Optional[Any] = None,
    timeout: int = 60
) -> Tuple[int, bytes, str]:
    """
    Executes a single HTTP request to Gemini Generative Language API.
    Supports dependency-injected transport for hermetic mock testing.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    data_bytes = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    # Mock transport hook for zero-quota unit testing
    if transport is not None:
        return transport(model, url, headers, payload)

    req = urllib.request.Request(url, data=data_bytes, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = resp.getcode()
            resp_body = resp.read()
            return status_code, resp_body, "OK"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        return e.code, err_body.encode("utf-8"), err_body
    except urllib.error.URLError as e:
        return 0, b"", f"Network error: {str(e.reason)}"
    except Exception as e:
        return 0, b"", f"Unexpected error: {str(e)}"


def parse_audio_response(resp_body_bytes: bytes) -> Tuple[bytes, int]:
    """Extracts raw PCM audio bytes and sample rate from the API response."""
    try:
        data = json.loads(resp_body_bytes.decode("utf-8"))
        candidates = data.get("candidates", [])
        if not candidates:
            raise GeminiTTSNonQuotaError("Malformed response: No candidates returned.")
        parts = candidates[0].get("content", {}).get("parts", [])
        for p in parts:
            inline = p.get("inlineData", {})
            if "audio" in inline.get("mimeType", ""):
                raw_b64 = inline.get("data", "")
                pcm_bytes = base64.b64decode(raw_b64)
                mime = inline.get("mimeType", "")
                rate = 24000
                if "rate=" in mime:
                    try:
                        rate = int(mime.split("rate=")[1].split(";")[0])
                    except (ValueError, IndexError):
                        rate = 24000
                return pcm_bytes, rate
        raise GeminiTTSNonQuotaError("Malformed response: No audio part found in candidates.")
    except json.JSONDecodeError as e:
        raise GeminiTTSNonQuotaError(f"Failed to parse JSON response: {str(e)}")


def strip_gemini_trailing_artifact(pcm_bytes: bytes, sample_rate: int) -> bytes:
    """
    Detects and surgically removes trailing Gemini TTS buffer overflow/pop artifacts.
    Gemini Generative Language TTS terminates PCM streams with ~100-200ms of corrupted
    buffer noise (clipping at amplitudes >25,000) after the actual speech has completed
    and dropped to silence.
    """
    try:
        import numpy as np
    except ImportError:
        return pcm_bytes

    data = np.frombuffer(pcm_bytes, dtype=np.int16).copy()
    if len(data) < int(sample_rate * 0.5):
        return pcm_bytes

    win_len = int(sample_rate * 0.005)  # 5ms windows
    n_windows = len(data) // win_len
    max_scan = min(n_windows, int(sample_rate * 0.6 / win_len))

    # Check if there is an artifact in the tail
    tail_chunk = data[-int(sample_rate * 0.05):].astype(float)
    has_burst = (np.max(np.abs(tail_chunk)) > 400) or (np.sqrt(np.mean(tail_chunk**2)) > 100)

    if not has_burst:
        return pcm_bytes

    silence_count = 0
    cut_idx = len(data)
    for w in range(n_windows - 1, n_windows - max_scan, -1):
        idx = w * win_len
        chunk = data[idx:idx + win_len].astype(float)
        rms = np.sqrt(np.mean(chunk**2))
        peak = np.max(np.abs(chunk))

        if rms < 35 and peak < 120:
            silence_count += 1
            if silence_count >= 6:  # 30ms of clean silence confirmed!
                cut_idx = idx + int(sample_rate * 0.02)  # Retain 20ms of silence
                break
        else:
            silence_count = 0

    clean_data = data[:cut_idx].copy()
    # Smooth 40ms cosine fade-out
    fade_len = min(len(clean_data), int(sample_rate * 0.04))
    if fade_len > 0:
        fade_curve = 0.5 * (1 + np.cos(np.linspace(0, np.pi, fade_len)))
        clean_data[-fade_len:] = (clean_data[-fade_len:].astype(float) * fade_curve).astype(np.int16)

    # Pad with 120ms of pure digital silence
    pad = np.zeros(int(sample_rate * 0.12), dtype=np.int16)
    sanitized = np.concatenate([clean_data, pad])
    return sanitized.tobytes()


def write_pcm_to_wav(pcm_bytes: bytes, sample_rate: int, output_wav_path: Path):
    """Writes linear 16-bit PCM mono bytes to standard WAV format, sanitized of Gemini tail pops."""
    clean_pcm = strip_gemini_trailing_artifact(pcm_bytes, sample_rate)
    output_wav_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(clean_pcm)


def measure_wav_duration(wav_path: Path) -> float:
    """Measures precise duration of a WAV file in seconds."""
    with wave.open(str(wav_path), "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return round(frames / float(rate), 2)


def normalize_to_ebu_r128(input_wav: Path, output_wav: Path) -> bool:
    """Normalizes audio to EBU R128 (-16 LUFS Integrated, True Peak < -1.0 dBFS)."""
    cmd = [
        "ffmpeg", "-y", "-i", str(input_wav),
        "-af", "loudnorm=I=-16:TP=-1.0:LRA=7",
        "-ar", "44100",
        str(output_wav)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Ensure normalized output wav has zero trailing pop
        try:
            import numpy as np
            with wave.open(str(output_wav), "rb") as wf:
                params = wf.getparams()
                data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).copy()
            cleaned_bytes = strip_gemini_trailing_artifact(data.tobytes(), params.framerate)
            with wave.open(str(output_wav), "wb") as wf:
                wf.setparams(params)
                wf.writeframes(cleaned_bytes)
        except Exception:
            pass
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        output_wav.write_bytes(input_wav.read_bytes())
        return False


def chunk_long_text_if_needed(text: str, max_chars: int = 4000) -> List[str]:
    """
    Chunks text strictly if it exceeds model technical threshold (default 4000 chars).
    Normal scripts are never chunked (1 single request).
    """
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return [cleaned]

    # Split at sentence boundaries
    sentence_endings = re.compile(r'([.!?؟\n]+)')
    tokens = sentence_endings.split(cleaned)
    chunks = []
    current_chunk = ""

    for i in range(0, len(tokens) - 1, 2):
        sent = tokens[i] + tokens[i + 1]
        if len(current_chunk) + len(sent) > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sent
        else:
            current_chunk += sent

    if len(tokens) % 2 == 1:
        current_chunk += tokens[-1]

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def synthesize_narration(
    text: str,
    voice: str,
    video_id: str = "production_video",
    style_instruction: str = DEFAULT_STYLE_INSTRUCTION,
    output_dir: Path = Path("public/audio"),
    transport: Optional[Any] = None,
    force_fresh: bool = False
) -> Dict[str, Any]:
    """
    Executes quota-aware, single-request speech synthesis with strict fallback hierarchy.
    Never probes models. Tries Priority 1 once; only falls back on authentic quota exhaustion.
    """
    # 1. Voice Validation Gate
    if voice not in ALLOWED_VOICES:
        raise GeminiTTSConfigurationError(
            f"Unauthorized voice '{voice}'. Allowed voices: {list(ALLOWED_VOICES.keys())}."
        )

    # 2. API Key Retrieval (Fail closed)
    api_key = get_sanitized_api_key()

    # 3. Check for extremely long text exception
    text_chunks = chunk_long_text_if_needed(text)
    is_chunked = len(text_chunks) > 1

    # 4. Cache Check (for single-chunk standard generation)
    cache_key = compute_cache_key(MODEL_PRIORITY[0], voice, DEFAULT_LANGUAGE, text, style_instruction)
    cached_wav = CACHE_DIR / f"{cache_key}.wav"
    cached_meta = CACHE_DIR / f"{cache_key}.meta.json"

    if not force_fresh and cached_wav.exists() and cached_meta.exists():
        try:
            meta = json.loads(cached_meta.read_text(encoding="utf-8"))
            dest_wav = output_dir / f"{video_id}_master_voice.wav"
            output_dir.mkdir(parents=True, exist_ok=True)
            dest_wav.write_bytes(cached_wav.read_bytes())
            duration = measure_wav_duration(dest_wav)
            return {
                "video_id": video_id,
                "requested_model": MODEL_PRIORITY[0],
                "actual_model": meta.get("actual_model", MODEL_PRIORITY[0]),
                "voice": voice,
                "request_count": 0,
                "fallback_used": meta.get("fallback_used", False),
                "fallback_reason": None,
                "audio_duration": duration,
                "cache_hit": True,
                "output_path": str(dest_wav),
                "status": "SUCCESS"
            }
        except Exception:
            pass  # If cache reading fails, proceed to live generation

    # 5. Live Synthesis with Sequential Quota-Aware Fallback
    request_count = 0
    fallback_used = False
    fallback_reason: Optional[str] = None
    actual_model: Optional[str] = None
    synthesized_pcm_chunks: List[bytes] = []
    final_sample_rate = 24000

    current_model_idx = 0

    while current_model_idx < len(MODEL_PRIORITY):
        candidate_model = MODEL_PRIORITY[current_model_idx]
        actual_model = candidate_model
        all_chunks_succeeded = True

        for chunk_idx, chunk_text in enumerate(text_chunks):
            payload = build_gemini_payload(chunk_text, voice, style_instruction)
            request_count += 1

            status_code, resp_bytes, err_msg = send_gemini_request(
                candidate_model, payload, api_key, transport=transport
            )

            if status_code == 200:
                pcm_bytes, rate = parse_audio_response(resp_bytes)
                synthesized_pcm_chunks.append(pcm_bytes)
                final_sample_rate = rate
            else:
                resp_str = resp_bytes.decode("utf-8", errors="replace")
                if is_authentic_quota_failure(status_code, resp_str):
                    fallback_used = True
                    fallback_reason = f"HTTP {status_code}: Quota / Rate-Limit Exhausted on {candidate_model}"
                    all_chunks_succeeded = False
                    synthesized_pcm_chunks.clear()
                    break  # Break out to try next candidate model
                else:
                    # Non-quota error (401, 403, 400 schema error, network bug)
                    raise GeminiTTSNonQuotaError(
                        f"Non-quota failure on model '{candidate_model}' with code {status_code}: {resp_str[:250]}"
                    )

        if all_chunks_succeeded:
            # Model generation succeeded!
            break
        else:
            # Step down exactly one level in priority hierarchy
            current_model_idx += 1

    # 6. Evaluation of Fallback Chain Result
    if not synthesized_pcm_chunks:
        raise GeminiTTSQuotaError(
            f"CRITICAL: All Gemini TTS models ({MODEL_PRIORITY}) exhausted their quota / rate limits. "
            f"Last reason: {fallback_reason}. Halting generation without burning quota."
        )

    # 7. Write Combined PCM Output
    full_pcm = b"".join(synthesized_pcm_chunks)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_wav_path = output_dir / f"{video_id}_voice_raw.wav"
    norm_wav_path = output_dir / f"{video_id}_master_voice.wav"

    write_pcm_to_wav(full_pcm, final_sample_rate, raw_wav_path)
    normalize_to_ebu_r128(raw_wav_path, norm_wav_path)
    duration = measure_wav_duration(norm_wav_path)

    # 8. Save to Cache
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cached_wav.write_bytes(norm_wav_path.read_bytes())
        meta_info = {
            "requested_model": MODEL_PRIORITY[0],
            "actual_model": actual_model,
            "voice": voice,
            "language": DEFAULT_LANGUAGE,
            "fallback_used": fallback_used,
            "fallback_reason": fallback_reason,
            "duration": duration,
            "chunk_count": len(text_chunks)
        }
        cached_meta.write_text(json.dumps(meta_info, indent=2), encoding="utf-8")
    except Exception:
        pass

    # 9. Return Structured Accounting Log
    return {
        "video_id": video_id,
        "requested_model": MODEL_PRIORITY[0],
        "actual_model": actual_model,
        "voice": voice,
        "request_count": request_count,
        "fallback_used": fallback_used,
        "fallback_reason": fallback_reason,
        "audio_duration": duration,
        "cache_hit": False,
        "output_path": str(norm_wav_path),
        "status": "SUCCESS"
    }


def run_preflight_sample(
    voice: str,
    output_dir: Path = Path("public/audio"),
    transport: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Synthesizes exactly ONE 10-15s preflight sample for user evaluation.
    Requires explicit user approval before final full narration generation.
    """
    print(f"--- RUNNING GEMINI TTS PREFLIGHT CHECK ---")
    print(f"Selected Voice: {voice} ({ALLOWED_VOICES.get(voice, {}).get('desc')})")
    print(f"Target Primary Model: {MODEL_PRIORITY[0]}")
    print(f"Preflight Sample Text: \"{CANONICAL_PREFLIGHT_TEXT}\"")

    res = synthesize_narration(
        text=CANONICAL_PREFLIGHT_TEXT,
        voice=voice,
        video_id="preflight_sample",
        output_dir=output_dir,
        transport=transport,
        force_fresh=True
    )

    print(f"\nPREFLIGHT SYNTHESIS COMPLETE:")
    print(f"  Model Used: {res['actual_model']}")
    print(f"  Fallback Triggered: {res['fallback_used']} ({res['fallback_reason']})")
    print(f"  Audio Duration: {res['audio_duration']}s")
    print(f"  Output: {res['output_path']}")
    print(f"  Requests Consumed: {res['request_count']}")
    return res


if __name__ == "__main__":
    print("Quota-Aware Gemini TTS Engine Loaded.")
    print(f"Model Hierarchy: {' -> '.join(MODEL_PRIORITY)}")
    print(f"Selectable Voices: {list(ALLOWED_VOICES.keys())}")
