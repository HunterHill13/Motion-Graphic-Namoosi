# DEPENDENCY & REPOSITORY AUDIT (v2 UPGRADE)

**Target:** AI Cinematic Motion-Graphics Agent Skill v2 (Living Motion + Voice Director + Natural Persian TTS)  
**Audit Date:** 2026-10-04  
**Auditor:** Senior AI Video Pipeline Architect  

---

## 1. Executive Matrix of Reference Repositories

| Repository | Origin / License | Evaluated Assets & Capabilities | v2 Reuse & Extension Strategy |
|---|---|---|---|
| **remotion-dev/skills** | Remotion Official / MIT | Official agent skills (`remotion-render`, `remotion-studio`, `remotion-best-practices`, `@remotion/captions`). | **Reuse 100%:** Keep core rendering, studio server, and caption infrastructure intact. |
| **anything2explainer** | Vincent Wei / PolyForm Noncommercial 1.0.0 | CV QC scripts (`motion_check.py`, `frame_metrics.py`), Star/Dot fields, `subs.ts` and `timeline.ts` data contracts. | **Reuse & Extend:** Retain quantitative QC. Expand `selfcheck.py` to audit Living Motion flags and audio stem validity. |
| **video-shotcraft** | Ding200602 / Apache 2.0 | Shot recipe cards, `aesthetic-rules.md` (R1-R4, Q1-Q10), sound design layering, musical beat syncing. | **Incorporate into Living Motion:** Adapt multi-beat kinetic cuts, riser-impact synchronization, and 3D zoom legibility. |
| **video-talkcraft** | Vincent Wei / PolyForm Noncommercial 1.0.0 | 7-layer shot model, `CameraRig` continuous motion, `Live demoteAt` state machine, anti-slideshow rules. | **Extend to v2:** Evolve continuous scale into multi-layer parallax and organic drifting noise. |
| **claude-remotion-skill** | haidrrrry / MIT | 60/30/10 palette rule, multi-property spring entrances, procedural noise grains. | **Reuse & Deepen:** Use mathematical spring configs (`damping: 20`, `stiffness: 120`) as baseline for secondary physics. |
| **claude-skill-motion-graphics** | docusphere / Community | Canonical Beat Sheet specification, Style Lock prompts (`STYLE_IMAGE`, `STYLE_VIDEO`, `AVOID`). | **Reuse:** Retain in `templates/beat-sheet.yaml` and `templates/style-lock.yaml`. |

---

## 2. Audio & Persian TTS External Engine Evaluation

Microsoft / Azure Persian TTS (`fa-IR-DilaraNeural`, `fa-IR-FaridNeural`) is **explicitly disqualified as the default** due to rigid prosody, robotic cadence, and poor handling of colloquial Persian rhythm.

### 2.1 Evaluated Engines for Natural Persian Narration

| Engine / Model | Architecture & Source | Quality & Naturalness | Latency & Local Support | v2 Role & Verdict |
|---|---|---|---|---|
| **Gemini TTS / Cloud Speech** | Google Cloud Gemini Multimodal Audio | **Tier 1 (High)**: Exceptional contextual intonation, natural Persian phrasing, human breath pauses. | Cloud API, requires API Key. | **Primary Cloud Engine:** Default for production explainers when cloud access is enabled. |
| **ElevenLabs Multilingual v2** | ElevenLabs Neural Flow Matching | **Tier 1 (High)**: Deep cinematic resonance, emotional range, realistic whisper/emphasis. | Cloud API, paid tier. | **Cinematic Cloud Engine:** Option for dramatic documentary & film modes. |
| **Aava Persian TTS** (`KEYHAN-A/aava-tts-persian-3b`) | HuggingFace / Diffusion-Transformer | **Tier 1 (High)**: Trained specifically on modern Persian prose and literary texts; native ezafe support. | Local Python / PyTorch / GPU. | **Flagship Open-Source Engine:** Evaluated in benchmark suite. |
| **Pocket TTS Farsi v2** (`mehdi-hf/pocket-tts-farsi`) | HuggingFace / Lightweight VITS/FastSpeech | **Tier 2 (Good)**: Clean articulation, minimal resource footprint, fast CPU inference. | Local Python / ONNX / CPU-friendly. | **Default Local / Offline Engine:** Excellent fallback when no cloud keys are provided. |
| **ddehghan/farsi-tts** | Coqui TTS / Tacotron2 adapted for Persian | **Tier 3 (Fair)**: Good phonetic accuracy but slight synthetic buzz. | Local Python. | **Secondary Local Fallback.** |
| **Edge-TTS (`fa-IR`)** | Microsoft Edge Cloud | **Tier 4 (Robotic)**: Monotone, frequent mispronunciations of silent ezafe. | Free cloud, zero config. | **Emergency Fallback Only:** Strictly not default. |

---

## 3. Licensing & Attribution Strategy

All third-party code, algorithms, and models comply with respective licenses:
- PolyForm Noncommercial 1.0.0 modules (`anything2explainer`, `video-talkcraft`) are credited in `ATTRIBUTIONS.md`.
- Apache 2.0 assets (`video-shotcraft`) retain original copyright headers and notice entries.
- MIT assets (`remotion-dev`, `claude-remotion-skill`) retain MIT license blocks.
- Open-source Persian TTS weights (HuggingFace Apache 2.0 / MIT) are invoked via standalone scripts without violating license bounds.
