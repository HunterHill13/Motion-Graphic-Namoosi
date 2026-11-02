# Capability Consolidation Matrix

## 1. Overview & Decision Framework
This matrix establishes the definitive architectural decisions for all capabilities developed from V1 to V40.1.
Every candidate implementation is classified into one of six rigid statuses:
- **`KEEP`**: Current implementation is already optimal, production-proven, and architecturally clean.
- **`MERGE`**: Valuable, distinct aspects from multiple implementations are unified into a single clean module.
- **`REFACTOR`**: Capability is indispensable, but implementation requires modular extraction or decoupling.
- **`REPLACE`**: A strictly superior alternative exists and replaces the older approach.
- **`ARCHIVE`**: Historical benchmark/lab with no active production role, preserved in `archive/` for scientific audit.
- **`DELETE`**: Deprecated, duplicate, broken, or anti-pattern code that is actively harmful or clutter.

---

## 2. Master Consolidation Matrix Table

| Capability | V# Origin | Candidate Implementations | Best Implementation | Why | Production Used | Final Location | Old Versions | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Authored Curves** | V27 | `evaluateAuthoredKeyframeTrack`, standard Remotion `interpolate` | V40.1 `AuthoredKeyframeEngine.ts` | Allows micro-frame authored roles (anticipation, launch, impact, settle) without robotic easing | YES (V40.1 Plinths) | `src/motion/curves/AuthoredKeyframeEngine.ts` | V27, V34 | **KEEP** |
| **Physical Bounce** | V28 | `PhysicalBounceRecipe.ts`, `V28_BounceLab.tsx` | V28 `PhysicalBounceRecipe.ts` | Complete closed-form physics ($y = y_0 + \frac{1}{2}gt^2$), COR decay, 2f squash | Secondary in V40.1 | `src/motion/physics/PhysicalBounceRecipe.ts` | V28 Lab | **KEEP** |
| **Kinematic Personalities** | V25 | `MotionFidelityEngine.ts` (8 profiles), simple CSS cubic-bezier | V25 `MotionFidelityEngine.ts` | Provides C0/C1/C2 continuous velocity evaluation across 8 material profiles | YES | `src/motion/fidelity/MotionFidelityEngine.ts` | V18, V25 labs | **KEEP** |
| **2D → 3D Transformation** | V29 | V29 Lab, V36.5 Craft Masterpiece, V38 Benchmark, V40.1 Monolith | V36.5 + V40.1 hybrid | Continuous topological slicing, dynamic rim lighting, zero-subpixel distortion | YES (V40.1 Monolith Spine) | `src/motion/transformation/` | V29, V30, V36, V37 | **MERGE** |
| **Causal Event Graph** | V21 | `ChoreographyEventGraph.ts`, Video-Talkcraft Causal Planning | V40.1 Video-Talkcraft Causal Graph | Every visual element requires a visible cause; completely halts unmotivated pop-ins | YES (V40.1) | `.agents/skills/cinematic-motion-director/references/causal-planning.md` + `src/choreography/` | V21, V24 | **KEEP** |
| **Element Budgeting** | V40.1 | Ad-hoc layers, V40.1 $\le 7$ budget | V40.1 Element Budget Discipline | Prevents visual multitasking and HUD cognitive overload | YES (V40.1) | Skill Core Standard (`SKILL.md`) | None | **KEEP** |
| **No-Orphan Discipline** | V40.1 | Orphan UI lingering, V40.1 Handoff/Dissolve | V40.1 No-Orphan Standard | Enforces that all visual elements either fuse into the substrate or exit via momentum | YES (V40.1) | Skill Core Standard (`SKILL.md`) | None | **KEEP** |
| **Intentional Stillness** | V13 | V13 reading windows, V40.1 1.0–2.5s Stillness | V40.1 Intentional Stillness Gate | Eliminates camera breathing/jitter during key information absorption | YES (V40.1 F465–F570) | Skill Core Standard (`SKILL.md`) | V13 | **KEEP** |
| **Motion-Carry Transitions** | V13 | `carryTransitions.ts`, hard cuts | V13 `carryTransitions.ts` | Transmits exit velocity vectors into next scene entrance | YES | `src/transition/carryTransitions.ts` | V13 | **KEEP** |
| **Motivated 3D Camera** | V13 | `CameraRig.tsx`, `cameraGrammar.ts`, V40.1 crane/orbit | V40.1 Unified Camera Rig | Ties camera moves to narrative scope (crane pull-back on climax) | YES (V40.1) | `src/camera/CameraGrammarRig.tsx` | V3, V13, V16 | **REFACTOR** |
| **Seismic Shock Reaction** | V25 | V25 Heavy Impact, V40.1 Landing Kick | V40.1 Camera Shock Kick | 3-frame damped vertical kick gives physical weight to mass landings | YES (V40.1) | `src/camera/CameraGrammarRig.tsx` | V25 | **MERGE** |
| **Zero-Subpixel Typography** | V16 | `typographyBehaviors.ts`, V25 Slam, V40.1 Sanitizer | V40.1 Integer Pixel & GPU Lock | Eliminates rasterization blur and fractional text vibration on high-DPI displays | YES (V40.1) | `src/typography/KineticTypography.tsx` | V16, V18, V25 | **REFACTOR** |
| **Dual Script Sanitizer** | V40 | Inline regex in V40.1, V39 diacritic rendering | V40.1 `sanitizeForDisplay` | Decouples phonetic TTS `speechText` from visual display `displayText` | YES (V40.1) | `src/typography/persianSanitizer.ts` | V39 | **REFACTOR** |
| **Voice Engine** | V1 | Edge-TTS (`fa-IR-FaridNeural`), Azure Neural, Gemini 2.5 TTS (`Puck`) | Google Gemini Multimodal Audio API (`gemini-2.5-flash-preview-tts` / `Puck`) | Superior Persian natural prosody, zero robotic artifacting, authoritative tone | YES (V40.1) | `projects/band-kaf/audio/` & Skill Reference | Edge-TTS, Azure | **REPLACE** (Banned Edge-TTS) |
| **Master Audio Ducking** | V4 | `build_master_audio_mix.py`, `build_preview_audio.py` | V40.1 `build_preview_audio.py` | Automated -14 dB dynamic sidechain ducking + EBU R128 loudness normalization | YES (V40.1) | `projects/band-kaf/audio/build_audio.py` | V4, V39 | **KEEP** |
| **Frame Metrics & Freeze QA** | V1 | `scripts/frame_metrics.py`, `scripts/motion_check.py` | V1 `frame_metrics.py` | OpenCV SSIM + pixel difference checking detects accidental freezes | YES | `scripts/qc/frame_metrics.py` | None | **KEEP** |
| **Quality Release Gates** | V5 | 6-Gate, 8-Point Adversarial, 13-Gate QC | V40.1 13 Automated Release Gates | Comprehensive pre-render validation preventing regressions | YES | Skill Core Standard (`SKILL.md`) | V5, V18 | **KEEP** |
| **Historical Showcase Labs** | V1–V38 | 38 individual composition files in `precision_lab` | Individual laboratory proofs | Historical research milestones; not part of active production pipeline | NO (Historical only) | `archive/legacy_labs/` | V1–V38 | **ARCHIVE** |
| **V39 Band Kaf Composition** | V39 | `V39_BandKafProduction.tsx` | `V39_BandKafProduction.tsx` | Failed production run (slideshow structure, Edge-TTS fallback); preserved for anti-pattern audit | NO (Superseded) | `archive/experiments/v39/` | V39 | **ARCHIVE** |
| **V40.1 Monolith Preview** | V40.1 | `V40_KineticMonolithPreview.tsx` | `V40_KineticMonolithPreview.tsx` | Active production flagship component for Band Kaf Acts 1 & 2 | YES | `projects/band-kaf/compositions/V40_KineticMonolithPreview.tsx` | V40 | **KEEP** |
| **Dead Composition Imports** | V1–V38 | 1500+ lines in `Root.tsx` | Clean, minimal `Root.tsx` | Clutters compilation, slows down Remotion Studio, causes confusion | NO | Removed from `Root.tsx` | V1–V38 entries | **DELETE FROM ROOT** |

---

## 3. Consolidation Action Plan

### 3.1 What is Kept & Promoted to Core
1. `AuthoredKeyframeEngine.ts` $\to$ Promoted to `src/motion/curves/AuthoredKeyframeEngine.ts`.
2. `PhysicalBounceRecipe.ts` $\to$ Maintained in `src/motion/physics/PhysicalBounceRecipe.ts`.
3. `MotionFidelityEngine.ts` $\to$ Maintained in `src/motion/fidelity/MotionFidelityEngine.ts`.
4. `carryTransitions.ts` $\to$ Maintained in `src/transition/carryTransitions.ts`.
5. `cameraGrammar.ts` & `CameraGrammarRig.tsx` $\to$ Maintained in `src/camera/`.
6. Google Gemini TTS Pipeline (`gemini-2.5-flash-preview-tts` / `Puck`) $\to$ Maintained as exclusive voice standard.
7. 13-Gate QC & Causal Planning Standards $\to$ Cemented in `.agents/skills/cinematic-motion-director/`.

### 3.2 What is Refactored / Modularized
1. `sanitizeForDisplay(text)`: Extracted from `V40_KineticMonolithPreview.tsx` into a dedicated production module `src/typography/persianSanitizer.ts`.
2. `Root.tsx`: Completely refactored from 1,757 lines down to < 100 lines, registering only active production compositions (`ProductionMaster`, `DevelopmentPreview`, `MotionLabGallery`).

### 3.3 What is Archived
1. Historical project test suites (`projects/persian_editorial_motion_test_v...`, `projects/stress_test_...`) $\to$ Moved to `archive/legacy_projects/`.
2. Historical precision labs (`src/motion/precision_lab/V27_...` through `V38_...`) $\to$ Moved to `archive/legacy_labs/`.
3. Failed V39 production attempt (`V39_BandKafProduction.tsx`) $\to$ Moved to `archive/experiments/v39/`.

### 3.4 What is Deleted
1. Obsolete Edge-TTS / Azure neural audio references across all template configurations.
2. Dead composition registrations in `Root.tsx`.
