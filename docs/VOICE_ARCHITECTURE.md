# VOICE DIRECTOR & NATURAL PERSIAN TTS SPECIFICATION (v2)

**Document:** `docs/VOICE_ARCHITECTURE.md`  
**Target:** Voice-First Authority, Dual-Clock Synchronization, Stem Mixing & Persian Naturalness  
**Date:** 2026-10-04  

---

## 1. The Voice-First Paradigm & Dual-Clock Authority

In cinematic film production, animation timing follows the recorded human voice — not the reverse.

### 1.1 Dual-Clock Contract
- **Physical Timing Clock = `VOICEOVER`:** The spoken `.wav` audio track and its extracted word timestamps define the exact frame indices where cuts, zooms, and visual hits occur.
- **Semantic Meaning Clock = `SCRIPT`:** The written script provides semantic grounding, typography text, and factual assertions for research cross-validation.
- If audio duration diverges from estimated reading speed, the **audio duration wins**; visuals stretch or compress to match word boundaries.

---

## 2. Natural Persian Voice System

### 2.1 The Problem with Microsoft/Azure Persian TTS
Engines like `fa-IR-DilaraNeural` and `fa-IR-FaridNeural`:
1. Use monotonous, repetitive pitch contours unsuited for documentary storytelling.
2. Frequently fail to enunciate the grammatical Persian **ezafe** (the unstressed `-e` or `-ye` connecting nouns and adjectives), rendering scientific prose ungrammatical.
3. Pronounce loanwords and medical acronyms with severe robotic distortion.

### 2.2 Evaluated Alternative Engines

| Engine | Type | Pros | Cons | Priority |
|---|---|---|---|---|
| **Gemini TTS / Cloud Audio** | Neural Multimodal | Human-like pacing, natural breath intake, contextual intonation. | Requires Google Cloud / Gemini API key. | **Tier 1 (Recommended Cloud)** |
| **ElevenLabs Multilingual v2** | Diffusion / Flow Matching | Rich timbre, deep emotional resonance, cinema-grade clarity. | Commercial API cost. | **Tier 1 (Cinematic Option)** |
| **Aava Persian TTS (`KEYHAN-A/aava-tts-persian-3b`)** | Open Source Transformer | Native Iranian accent, trained on classical & modern Persian prose. | Requires local GPU/VRAM. | **Tier 1 (Open-Source Flagship)** |
| **Pocket TTS Farsi v2 (`mehdi-hf/pocket-tts-farsi`)** | Lightweight VITS/ONNX | Highly efficient, runs smoothly on CPU, natural sentence cadence. | Slightly less emotional range than 3B models. | **Tier 2 (Default Local Fallback)** |
| **Edge-TTS (`fa-IR`)** | Fallback Cloud | Zero API keys, universally available. | Monotone cadence, robotic. | **Tier 4 (Emergency Fallback Only)** |

---

## 3. Persian Text Optimization Pipeline (`audio/engine/PersianTextOptimizer.py`)

Before text is sent to any TTS model, it must pass through automated normalization:
1. **Half-Space (Zero-Width Non-Joiner - ZWNJ) Normalization:**
   - Standardizes prefixes (`می‌شود`, `نمی‌تواند`) and plural suffixes (`سلول‌ها`, `پروتئین‌ها`).
2. **Ezafe Diacritic Insertion:**
   - Detects noun-adjective pairs and attaches short-vowel marks (`ِ` or `یِ`) where needed for correct phonetic pronunciation.
3. **Number & Date Expansion:**
   - Converts digits to Persian words (`۱۴۰۳` $\to$ `یک هزار و چهارصد و سه`, `۲۵%` $\to$ `بیست و پنج درصد`).
4. **Scientific & Medical Loanword Transliteration:**
   - Phonetically respells complex terms (e.g., `Apoptosis` $\to$ `آپوپتوز`, `Cytochrome c` $\to$ `سیتوکروم سی`).

---

## 4. Audio Stem Architecture & Automated Ducking

The final video audio is assembled from 3 discrete stems:
```text
audio/
├── narration/      # Isolated clean voice recording (processed, normalized to -19 LUFS)
├── music/          # Cinematic background music track (-22 LUFS)
├── sfx/            # Sound design hits, whooshes, risers, and UI clicks (-18 LUFS)
└── mixed/          # Master render stem mixed down to -16 LUFS
```

### 4.1 Dynamic Ducking Rules (`audio/mixer/StemMixer.py`)
- When narration speech is detected (amplitude threshold $> -40\,\text{dB}$):
  - Music volume is automatically ducked by **$-14\,\text{dB}$**.
  - Duck attack time: $120\,\text{ms}$ (smooth fade before first syllable).
  - Duck release time: $350\,\text{ms}$ (gentle return after sentence pause).
- SFX elements duck music momentarily by **$-6\,\text{dB}$** on major cinematic impacts.

---

## 5. Persian Voice Benchmark Suite (`audio/voice-benchmark/`)

A dedicated evaluation suite to quantitatively compare engines across:
- **Naturalness & MOS Score.**
- **Pronunciation accuracy on medical terms.**
- **Latency (seconds to generate 30s audio).**
- **Hardware resource consumption (RAM / VRAM).**
