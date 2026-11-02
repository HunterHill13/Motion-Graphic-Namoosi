# Complete Capability Inventory (V1 → V40.1)

## Executive Summary
This document provides a comprehensive, rigorous inventory of every significant capability developed across the 40 iteration cycles of the Cinematic Motion Graphics Engine. In accordance with the non-negotiable architectural directives:
- **Capability ≠ Implementation ≠ File ≠ Version.**
- Historical experiments are evaluated strictly on their proven, runtime-evaluated, and pixel-verified contributions.
- The goal is **capability preservation and consolidation**, eliminating dead code and laboratory clutter while ensuring zero regression in production capabilities.

---

## 1. Motion Subsystem

### 1.1 Authored Keyframes & Temporal Curves
* **CAPABILITY:** Authored Keyframes & Non-Linear Temporal Curve Parameterization
* **FIRST INTRODUCED:** V27 (`src/motion/curves/AuthoredKeyframeEngine.ts`)
* **BEST KNOWN VERSION:** V40.1 (`src/motion/curves/AuthoredKeyframeEngine.ts` evaluated in `V40_KineticMonolithPreview.tsx`)
* **CURRENT IMPLEMENTATION:** Multi-segment keyframe tracks with semantic roles (`REST`, `ANTICIPATION`, `LAUNCH`, `PEAK`, `IMPACT`, `OVERSHOOT`, `SETTLE`) and cubic bezier evaluators.
* **CURRENT LOCATION:** `src/motion/curves/AuthoredKeyframeEngine.ts`
* **ACTUALLY USED IN PRODUCTION:** YES (Drives Plinth 1, Plinth 2, and Plinth 3 in V40.1).
* **RUNTIME VERIFIED:** YES (Verified in `V40.1_INTEGRATION_VERIFICATION.md`).
* **PIXEL VERIFIED:** YES (Observable in `renders/v40/V40.1_PREVIEW_KINETIC_MONOLITH.mp4` F130-F465).
* **SUPERSEDED BY:** N/A (Current production gold standard).
* **DEPENDENCIES:** Remotion `interpolate`, `Easing`.
* **STATUS:** **KEEP**
* **REASON:** Foundational to eliminating procedural robotic linear interpolation; gives micro-frame directorial authority.

---

### 1.2 Anticipation & Hydraulic Pre-Roll
* **CAPABILITY:** Elastic & Hydraulic Anticipation (Negative Pre-Roll Dip)
* **FIRST INTRODUCED:** V18 (`Benchmark1_KineticTypeSlam`) / V25 (`MotionFidelityEngine.ts`)
* **BEST KNOWN VERSION:** V40.1 (`PLINTH_1_TRACK` anticipation curve)
* **CURRENT IMPLEMENTATION:** Negative offset curve (-16px dip over 25 frames before upward explosive launch).
* **CURRENT LOCATION:** `src/motion/curves/AuthoredKeyframeEngine.ts` & `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES (F135-F155 in V40.1).
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** `AuthoredKeyframeEngine.ts`
* **STATUS:** **KEEP**
* **REASON:** Satisfies Disney Principle #2 and prevents jarring instant acceleration.

---

### 1.3 Physical Gravitational Bounce & Contact Dynamics
* **CAPABILITY:** Parabolic Gravitational Bounce with Coefficient of Restitution (COR) and Contact Squash
* **FIRST INTRODUCED:** V28 (`src/motion/physics/PhysicalBounceRecipe.ts` / `V28_BounceLab.tsx`)
* **BEST KNOWN VERSION:** V28 (`PhysicalBounceRecipe.ts`)
* **CURRENT IMPLEMENTATION:** Closed-form parabolic motion $y(t) = apexY + 0.5 g t^2$ with decaying rebound apex heights, 2-frame floor squash window conserving volume ($s_x \cdot s_y = 1$), and deterministic settle threshold.
* **CURRENT LOCATION:** `src/motion/physics/PhysicalBounceRecipe.ts`
* **ACTUALLY USED IN PRODUCTION:** Partial (Used as secondary impact logic; full multi-bounce was showcased in V28/V34).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES (Verified in `renders/v28/V28_PRODUCTION_MASTER.mp4`).
* **SUPERSEDED BY:** Adapted into single-impact snap settle in V40.1.
* **DEPENDENCIES:** Remotion core.
* **STATUS:** **KEEP AS REUSABLE RECIPE**
* **REASON:** Perfect physical formulation for falling/rebounding bodies; essential for future physical simulations.

---

### 1.4 Spring Physics & Damped Harmonic Oscillations
* **CAPABILITY:** Mass-Spring-Damper Physical Simulation
* **FIRST INTRODUCED:** V3 (`StressTestMain.tsx`) / V18 (`src/motion/recipes/ElasticSnappingRecipe.ts`)
* **BEST KNOWN VERSION:** V34 / V40.1 (`spring` from Remotion with mass 1.8, stiffness 180, damping 26)
* **CURRENT IMPLEMENTATION:** Remotion native `spring` parameterization mapped to architectural mass.
* **CURRENT LOCATION:** `src/motion/recipes/ElasticSnappingRecipe.ts` & Remotion built-in.
* **ACTUALLY USED IN PRODUCTION:** YES (Drives secondary trusses and camera shock in V40.1).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** Hybridized with `AuthoredKeyframeEngine` in V40.1.
* **DEPENDENCIES:** `remotion`.
* **STATUS:** **KEEP**
* **REASON:** Indispensable for organic micro-settles where manual keyframing would feel stiff.

---

### 1.5 Intentional Stillness & Reading Holds
* **CAPABILITY:** Intentional Stillness (1.0s – 2.5s Zero-Jitter Post-Impact Cognitive Hold)
* **FIRST INTRODUCED:** V13 (`cameraGrammar.ts` reading windows) / Formally systematized in V40.1 via Video-Talkcraft.
* **BEST KNOWN VERSION:** V40.1 (`references/causal-planning.md` + `V40_KineticMonolithPreview.tsx`)
* **CURRENT IMPLEMENTATION:** Hard clamps on transform styles post-settle, halting micro-drifts and camera oscillations during viewer reading phases.
* **CURRENT LOCATION:** `src/motion/precision_lab/V40_KineticMonolithPreview.tsx` (F465–F570).
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES (Monolith trilogy hold F465–F570).
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Timing logic.
* **STATUS:** **KEEP**
* **REASON:** Resolves the critical "hyperactive camera jitter" defect; essential for human reading comprehension.

---

### 1.6 Momentum Transfer & Kinetic Pulse
* **CAPABILITY:** Inter-Object Momentum Handoff (Kinetic Pulse along architectural rails)
* **FIRST INTRODUCED:** V26 (`StudyD_PhysicalSceneHandoff.tsx`) / V29 (`TransformationContinuityEngine.ts`)
* **BEST KNOWN VERSION:** V40.1 (`V40_KineticMonolithPreview.tsx` F215–F238 and F320–F355)
* **CURRENT IMPLEMENTATION:** Primary object deceleration computes terminal velocity vector, which injects kinetic energy into connecting rails/arcs, initiating secondary object ascent.
* **CURRENT LOCATION:** `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Remotion interpolation.
* **STATUS:** **KEEP & GENERALIZE**
* **REASON:** Eliminates unmotivated isolated triggers; forms the core of mechanical causality.

---

## 2. Transformation Subsystem

### 2.1 Continuous 2D → 3D Topological Transformation
* **CAPABILITY:** Continuous 2D Emblem to 3D Extruded Monolith via Slicing and Orbit
* **FIRST INTRODUCED:** V29 (`V29_TransformationLab.tsx`)
* **BEST KNOWN VERSION:** V36.5 (`V36_5_CraftMasterpiece.tsx`) / V38 (`V38_ShowreelBenchmark.tsx`)
* **CURRENT IMPLEMENTATION:** Multi-layer SVG slicing with pseudo-volumetric extrusion depth, dynamic edge shading, and gyroscopic perspective projection.
* **CURRENT LOCATION:** `src/motion/precision_lab/V36_5_CraftMasterpiece.tsx` & `src/motion/TransformationContinuityEngine.ts`
* **ACTUALLY USED IN PRODUCTION:** YES (Integrated into V40.1 Monolith central spine).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES (`renders/v36_5_craft/V36_5_CRAFT_MASTERPIECE.mp4`).
* **SUPERSEDED BY:** V40.1 Monolith environment.
* **DEPENDENCIES:** SVG path geometry + CSS 3D matrix.
* **STATUS:** **MERGE & PRESERVE IN CORE**
* **REASON:** Signature capability of the engine. Bridges graphic design and cinematic cinematography without Three.js overhead.

---

### 2.2 Vector Shape Morphing & Winding Alignment
* **CAPABILITY:** Perceptual Vector Path Morphing with Point Correspondence
* **FIRST INTRODUCED:** V18 (`Benchmark3_ShapeMorphToChart`) / V25 (`MotionFidelityEngine.ts`)
* **BEST KNOWN VERSION:** V25 (`src/motion/fidelity/MotionFidelityEngine.ts`)
* **CURRENT IMPLEMENTATION:** Point sampling, length normalization, rotational indexing alignment to minimize path tangling during interpolation.
* **CURRENT LOCATION:** `src/motion/fidelity/MotionFidelityEngine.ts`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES (`renders/v25/V25_05_CircleStarMorph.mp4`).
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** SVG path parsers.
* **STATUS:** **KEEP IN MOTION RECIPES**
* **REASON:** Critical for diagrammatic transitions (circles to polygons to data bars).

---

### 2.3 Volume & Mass Conservation in Deformation
* **CAPABILITY:** Physical Volume Conservation ($scaleX \cdot scaleY = 1.0$)
* **FIRST INTRODUCED:** V28 (`PhysicalBounceRecipe.ts`) / V29 (`TransformationContinuityEngine.ts`)
* **BEST KNOWN VERSION:** V29 & V40.1
* **CURRENT IMPLEMENTATION:** Whenever an element squashes along one axis, the orthogonal axis dilates by the exact reciprocal factor ($s_x = 1/s_y$).
* **CURRENT LOCATION:** `src/motion/TransformationContinuityEngine.ts`
* **ACTUALLY USED IN PRODUCTION:** YES (Impact zones and telescoping pillars).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Mathematics.
* **STATUS:** **KEEP**
* **REASON:** Prevents visual assets from feeling like rubber balloons or hollow illusions.

---

## 3. Choreography Subsystem

### 3.1 Causal Event Graph & Cause-Effect Linking
* **CAPABILITY:** Directed Causal Event Graph (Every visual state change has an explicit ancestor cause)
* **FIRST INTRODUCED:** V21 (`ChoreographyEventGraph.ts`) / Integrated formally with Video-Talkcraft in V40.1.
* **BEST KNOWN VERSION:** V40.1 (`docs/V40.1_CAUSAL_AUDIT.md` + `references/causal-planning.md`)
* **CURRENT IMPLEMENTATION:** Strict schema: `STATE -> ANTICIPATION -> CAUSE -> ACTION -> CONSEQUENCE -> SETTLE`. No element appears unsummoned.
* **CURRENT LOCATION:** `.agents/skills/cinematic-motion-director/references/causal-planning.md`
* **ACTUALLY USED IN PRODUCTION:** YES (100% of V40.1 transitions pass the 7 causal gates).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Directing methodology.
* **STATUS:** **KEEP AS CORE SKILL STANDARD**
* **REASON:** The single most decisive improvement separating professional motion design from amateur slide sequences.

---

### 3.2 Element Budgeting & No Orphan Discipline
* **CAPABILITY:** Strict Screen Element Budgeting ($\le 7$ Active) and Orphan Element Elimination
* **FIRST INTRODUCED:** V40.1 (Adapted from Video-Talkcraft methodology).
* **BEST KNOWN VERSION:** V40.1 (`SKILL.md` + `references/causal-planning.md`)
* **CURRENT IMPLEMENTATION:** Hard cap of 5–7 elements on screen. When an element's narrative utility concludes, it must fuse back into the architectural substrate or exit along a velocity vector.
* **CURRENT LOCATION:** `.agents/skills/cinematic-motion-director/SKILL.md`
* **ACTUALLY USED IN PRODUCTION:** YES (V40.1 maintains strictly 5 active elements across all acts).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Architectural planning.
* **STATUS:** **KEEP AS CORE SKILL STANDARD**
* **REASON:** Eliminates visual clutter, HUD overload, and wandering disconnected graphics.

---

### 3.3 Motion-Carry Transitions
* **CAPABILITY:** Cross-Cut Momentum Vector Preservation (Motion-Carry)
* **FIRST INTRODUCED:** V13 (`src/transition/carryTransitions.ts`)
* **BEST KNOWN VERSION:** V13 / V40.1 (`carryTransitions.ts` + Monolith camera pan handoff)
* **CURRENT IMPLEMENTATION:** Handoff of exit position, velocity, and rotation from scene $N$ into entrance trajectories of scene $N+1$.
* **CURRENT LOCATION:** `src/transition/carryTransitions.ts`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** Single-World Canvas (V40) makes cuts obsolete, but Motion-Carry remains vital for intra-world camera reframes.
* **DEPENDENCIES:** Remotion interpolation.
* **STATUS:** **KEEP AS SHARED SYSTEM**
* **REASON:** Crucial whenever multi-scene cuts are unavoidable.

---

## 4. Camera Subsystem

### 4.1 Directional Camera Grammar & Motivated Moves
* **CAPABILITY:** Motivated 3D Camera Rigs (Crane, Tracking, Orbit, Push, Pull)
* **FIRST INTRODUCED:** V13 (`src/camera/cameraGrammar.ts`)
* **BEST KNOWN VERSION:** V40.1 (Orbital tilt in Act 2, Crane pull-back in Act 7)
* **CURRENT IMPLEMENTATION:** Perspective-3D viewport manipulation synchronized with narrative weight. Crane pull-back expands field of view as narrative scope broadens.
* **CURRENT LOCATION:** `src/camera/cameraGrammar.ts` & `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES (F465–F570 crane shot).
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** CSS 3D transforms (`perspective`, `rotateX`, `rotateY`, `translateZ`).
* **STATUS:** **KEEP & CONSOLIDATE INTO CAMERA ENGINE**
* **REASON:** Prevents artificial zoom-and-pan; creates genuine cinematic parallax.

---

### 4.2 Camera Reaction to Seismic Impact
* **CAPABILITY:** Micro-Shock Camera Reaction to Mechanical Strike
* **FIRST INTRODUCED:** V25 (`V25_02_HeavyImpact.tsx`)
* **BEST KNOWN VERSION:** V40.1 (Plinth 3 landing impact F465)
* **CURRENT IMPLEMENTATION:** High-frequency, rapid-decay 3-frame vertical kick ($+8\text{px} \to -4\text{px} \to +1\text{px} \to 0\text{px}$) applied to camera viewpoint at point of physical contact.
* **CURRENT LOCATION:** `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Easing curves.
* **STATUS:** **KEEP**
* **REASON:** Makes visual impacts visceral and physically grounded.

---

## 5. Visual Design & Typography Subsystem

### 5.1 Zero-Subpixel-Jitter Persian Typography
* **CAPABILITY:** Persian RTL Kinetic Typography with Zero Subpixel Jitter & Hardware Pixel Locking
* **FIRST INTRODUCED:** V16 (`persian_editorial_motion_test_v16`) / V25 (`V25_10_KineticTypeSlam`)
* **BEST KNOWN VERSION:** V40.1 (`sanitizeForDisplay` + integer coordinates)
* **CURRENT IMPLEMENTATION:** 
  1. Complete suppression of fractional pixel translations (`Math.round` or CSS integer pixels).
  2. `backface-visibility: hidden` and `transform: translate3d(0,0,0)`.
  3. Strict isolation of diacritics (harakat/tashdid) from visual display string.
* **CURRENT LOCATION:** `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Web fonts (Vazirmatn).
* **STATUS:** **KEEP AS MANDATORY STANDARD**
* **REASON:** Completely eliminates the blurry text vibration bug on high-DPI displays.

---

### 5.2 Architectural Materiality & Lighting Model
* **CAPABILITY:** Multi-Pass Titanium Shading, Emissive Edge Lights, Volumetric Shadows
* **FIRST INTRODUCED:** V37.1 / V38
* **BEST KNOWN VERSION:** V40.1 (`V40_KineticMonolithPreview.tsx`)
* **CURRENT IMPLEMENTATION:** Dark titanium base (`#0B0D13`), directional cadmium/amber rim highlights (`#FF6A00`, `#FFAA00`), volumetric ambient drop shadows (`rgba(0,0,0,0.85)`).
* **CURRENT LOCATION:** `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** CSS linear/radial gradients, drop-shadow filters.
* **STATUS:** **KEEP IN PRODUCTION LIBRARY**
* **REASON:** Gives institutional and scientific content a premium, serious broadcast feel.

---

## 6. Audio Subsystem

### 6.1 Google Gemini Multimodal Audio Voice Engine
* **CAPABILITY:** Native Persian Voice Synthesis via Google Gemini Multimodal Audio API
* **FIRST INTRODUCED:** V40 (`projects/v40_audio/build_preview_audio.py`)
* **BEST KNOWN VERSION:** V40.1 (`projects/v40_audio/build_preview_audio.py` using `gemini-2.5-flash-preview-tts` and voice `Puck`)
* **CURRENT IMPLEMENTATION:** Direct REST call to `generativelanguage.googleapis.com`, exporting 24 kHz Linear PCM audio, normalized to EBU R128 (-16 LUFS).
* **CURRENT LOCATION:** `projects/v40_audio/build_preview_audio.py` & `.agents/skills/cinematic-motion-director/references/voice-director-and-persian-tts.md`
* **ACTUALLY USED IN PRODUCTION:** YES (`public/audio/v40_preview_master.mp3`).
* **RUNTIME VERIFIED:** YES
* **AUDIO VERIFIED:** YES
* **SUPERSEDED BY:** N/A (Edge-TTS and Azure are permanently banned).
* **DEPENDENCIES:** Python `requests`, `ffmpeg`.
* **STATUS:** **KEEP AS EXCLUSIVE VOICE ENGINE**
* **REASON:** Unmatched natural Persian prosody, zero robotic clipping, native institutional authority.

---

### 6.2 Dual-Representation Script Engine (Pronunciation Lock vs. Visual Display)
* **CAPABILITY:** Complete Decoupling of Phonetic Voice Script from Visual Display Text
* **FIRST INTRODUCED:** V40 (`V40_KineticMonolithPreview.tsx` / `sanitizeForDisplay`)
* **BEST KNOWN VERSION:** V40.1
* **CURRENT IMPLEMENTATION:**
  - `speechText`: Encodes exact Arabic/Persian diacritics (َ ِ ُ ّ ْ) to enforce correct syllable stress and prevent TTS hallucinations (e.g. «بَقِیَّتُ‌الله»).
  - `displayText`: Stripped clean via regex of all diacritics and normalized for clean Persian orthography (e.g. «بقیه‌الله»).
* **CURRENT LOCATION:** `src/motion/precision_lab/V40_KineticMonolithPreview.tsx`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Regular expressions.
* **STATUS:** **KEEP & MODULARIZE INTO `src/typography/persianSanitizer.ts`**
* **REASON:** Solves the core defect where TTS required diacritics that cluttered the visual graphic design.

---

### 6.3 Sidechain Ducking & Dynamic Master Audio Mixing
* **CAPABILITY:** Automated Audio Mastering with Voice-Activated Sidechain Ducking
* **FIRST INTRODUCED:** V4 (`build_master_audio_mix.py`)
* **BEST KNOWN VERSION:** V40.1 (`projects/v40_audio/build_preview_audio.py`)
* **CURRENT IMPLEMENTATION:** FFmpeg `sidechaincompress` filter dipping background music by -14 dB during vocal activity with 200ms attack and 800ms release, coupled with EBU R128 `loudnorm` filter.
* **CURRENT LOCATION:** `projects/v40_audio/build_preview_audio.py`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **AUDIO VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** FFmpeg CLI.
* **STATUS:** **KEEP AS REUSABLE AUDIO PIPELINE**
* **REASON:** Delivers broadcast-level vocal intelligibility without manual keyframing in a DAW.

---

## 7. Quality Assurance (QA) Subsystem

### 7.1 Quantitative Frame Metrics & Freeze Detection
* **CAPABILITY:** Automated Pixel Difference & Frozen Frame Detection
* **FIRST INTRODUCED:** V1 (`scripts/frame_metrics.py`, `scripts/motion_check.py`)
* **BEST KNOWN VERSION:** V1 (`scripts/frame_metrics.py`)
* **CURRENT IMPLEMENTATION:** OpenCV frame diffing, SSIM calculation, and zero-motion duration threshold alerts.
* **CURRENT LOCATION:** `scripts/frame_metrics.py` & `scripts/motion_check.py`
* **ACTUALLY USED IN PRODUCTION:** YES (Automated validation in CI/CD).
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Python `opencv-python`, `numpy`.
* **STATUS:** **KEEP IN SCRIPTS/TOOLING**
* **REASON:** Catches accidental frame freezes, stuck animations, or render drops automatically.

---

### 7.2 13 Automated Release Gates & Production Verification
* **CAPABILITY:** Multi-Gate Quality Gate Enforcement
* **FIRST INTRODUCED:** V5 (`docs/cinematic-quality-gates.md`) / Expanded to 13 gates in V40.1
* **BEST KNOWN VERSION:** V40.1 (`SKILL.md`)
* **CURRENT IMPLEMENTATION:** Release gate checklists covering voice prosody, causal links, element budget, typography jitter, and TypeScript compilation.
* **CURRENT LOCATION:** `.agents/skills/cinematic-motion-director/SKILL.md`
* **ACTUALLY USED IN PRODUCTION:** YES
* **RUNTIME VERIFIED:** YES
* **PIXEL VERIFIED:** YES
* **SUPERSEDED BY:** N/A
* **DEPENDENCIES:** Process.
* **STATUS:** **KEEP IN SKILL CORE**
* **REASON:** The definitive gatekeeper preventing regression and broken deliverables.

---

## 8. Historical Inventory Summary Table

| Category | Capability | Origin | Best Version | Action | Destination |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Motion** | Authored Keyframe Engine | V27 | V40.1 | **KEEP** | `src/motion/curves/` |
| **Motion** | Physical Gravitational Bounce | V28 | V28 | **KEEP** | `src/motion/physics/` |
| **Motion** | Kinematic Personalities (8 types) | V25 | V25 | **MERGE** | `src/motion/fidelity/` |
| **Motion** | Intentional Stillness (Holds) | V13 | V40.1 | **KEEP** | Skill & Production Core |
| **Motion** | Inter-Object Momentum Handoff | V26 | V40.1 | **KEEP** | Production Core |
| **Transform** | Continuous 2D → 3D Slice Extrusion | V29 | V36.5/V38 | **KEEP** | `src/motion/transformation/` |
| **Transform** | Shape Morphing & Winding | V18 | V25 | **KEEP** | `src/motion/recipes/` |
| **Transform** | Volume Conservation ($s_x s_y = 1$) | V28 | V40.1 | **KEEP** | `src/motion/physics/` |
| **Choreography** | Causal Event Graph Engine | V21 | V40.1 | **KEEP** | Skill & `src/choreography/` |
| **Choreography** | Element Budget ($\le 7$) & No-Orphan | V40.1 | V40.1 | **KEEP** | Skill Core Standard |
| **Choreography** | Motion-Carry Transitions | V13 | V13 | **KEEP** | `src/transition/` |
| **Camera** | Motivated 3D Camera Grammar | V13 | V40.1 | **KEEP** | `src/camera/` |
| **Camera** | Seismic Impact Reaction Kick | V25 | V40.1 | **KEEP** | `src/camera/` |
| **Typography** | Zero-Subpixel-Jitter RTL Typography | V16 | V40.1 | **KEEP** | `src/typography/` |
| **Typography** | Dual Script Sanitizer (`displayText`) | V40 | V40.1 | **EXTRACT** | `src/typography/` |
| **Visual Design** | Titanium / Cadmium Light Language | V37.1 | V40.1 | **PRESERVE** | `projects/band-kaf/` |
| **Audio** | Google Gemini Multimodal TTS | V40 | V40.1 | **KEEP** | Skill Core Mandate |
| **Audio** | Sidechain Ducking & EBU R128 Mix | V4 | V40.1 | **KEEP** | `scripts/audio/` |
| **QA** | OpenCV Frame Metrics & Freeze Check | V1 | V1 | **KEEP** | `scripts/qc/` |
| **QA** | 13-Gate Automated QC Protocol | V5 | V40.1 | **KEEP** | Skill Core Directive |
| **Compositions** | Historical Lab Compositions (V1–V38) | V1–V38 | V1–V38 | **ARCHIVE** | `archive/legacy_labs/` |
| **Compositions** | V39 Full Band Kaf (Slideshow) | V39 | V39 | **ARCHIVE** | `archive/experiments/v39/` |
| **Compositions** | V40.1 Monolith Preview Master | V40.1 | V40.1 | **KEEP** | `projects/band-kaf/compositions/` |
