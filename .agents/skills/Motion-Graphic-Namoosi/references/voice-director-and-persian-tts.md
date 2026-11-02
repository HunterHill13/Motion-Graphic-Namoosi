# Voice Director & Persian TTS Authority Reference

> **Mandate:** Quota-Aware Audio Authority  
> **Authorized Engine:** Google Gemini Multimodal Audio API (`https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`)  
> **Model Hierarchy:** `gemini-3.8-flash-tts` -> `gemini-3.8-flash-lite-tts` -> `gemini-3.1-flash-tts-preview`  
> **Approved Voices:** `Puck` (Male), `Callirrhoe` (Female)  
> **Doctrine:** ONE VIDEO = ONE TTS REQUEST, ZERO SPECULATIVE PROBING

---

## 1. The Voice Authority Contract

1. **`VOICEOVER = Physical Timing Truth`**: The synthesized Gemini audio waveform and its exact acoustic transients govern frame boundaries, cut points, camera accelerations, and impact hits.
2. **`SCRIPT = Semantic Meaning Truth`**: Spoken text provides institutional definitions, metrics, and on-screen typography.

---

## 2. Quota-Aware Architecture: Google Gemini Audio

### 2.1 Model Hierarchy & Quota Fallback Chain
- **Priority 1 (Default / Highest Quality):** `gemini-3.8-flash-tts`
- **Priority 2 (First Quota Fallback):** `gemini-3.8-flash-lite-tts` (Used ONLY upon authentic quota exhaustion)
- **Priority 3 (Final Quota Fallback):** `gemini-3.1-flash-tts-preview` (Legacy fallback)
- **Halt Condition:** If Priority 3 also encounters quota exhaustion, halt immediately and report `GeminiTTSQuotaError`.

### 2.2 Inviolable Rules
- **No Speculative Probing:** Never make pre-emptive requests to test which model works or compare quality.
- **Fail Closed on Credentials:** If `GEMINI_API_KEY` is missing, halt immediately. Never print or leak the key.
- **Non-Quota Errors Do Not Fall Back:** HTTP 400 (bad argument), 401 (unauthorized), or network bugs fail immediately without stepping down models.
- **One Video = One Request:** Pass the full video narration in a single request. Never chunk by scene.

---

## 3. Canonical Voice Synthesis Script (`scripts/synthesize_gemini_tts.py`)

Production projects execute synthesis via `scripts/synthesize_gemini_tts.py`:

```python
from scripts.synthesize_gemini_tts import synthesize_narration, run_preflight_sample

# Step 1: Preflight check (10-15s sample)
preflight_result = run_preflight_sample(voice="Puck")

# Step 2: Full video narration (after user approval)
res = synthesize_narration(
    text=full_persian_script,
    voice="Puck",
    video_id="my_production_video"
)
```

---

## 4. Audio Mastering Specification

- **Master Loudness Target:** EBU R128 (-16 LUFS Integrated, True Peak < -1.0 dBFS).
- **Format:** Linear PCM / WAV 24kHz / 44.1kHz mono.
- **Dynamic Sidechain Ducking:** -14 dB under vocal dialogue phrases.
