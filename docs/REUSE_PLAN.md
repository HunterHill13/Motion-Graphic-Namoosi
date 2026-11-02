# CODE REUSE & ADAPTATION PLAN (v2 UPGRADE)

**Target:** AI Cinematic Motion-Graphics Agent Skill v2  
**Date:** 2026-10-04  
**Principle:** *Zero unnecessary reinvention. Extract maximum value from audited libraries, then build clean architectural glue and missing cinematic intelligence.*

---

## 1. Concrete Inventory of Assets to Reuse vs. Adapt vs. Create

### 1.1 Direct Reuse (100% As-Is)

1. **Remotion Framework & CLI:**
   - Rendering infrastructure (`npx remotion render`).
   - Studio preview server (`npx remotion studio`).
   - Core packages: `@remotion/cli`, `@remotion/bundler`, `@remotion/captions`, `@remotion/shapes`, `@remotion/paths`.
2. **Background Procedural Effects:**
   - `src/effects/Grain.tsx` (SVG feTurbulence procedural film grain).
   - `src/effects/Grade.tsx` (CSS film grading overlays).
   - `src/effects/BgMesh.tsx` (Canvas / CSS animated radial gradient mesh).
   - `src/effects/DotFieldBg.tsx` & `StarFieldBg.tsx` (Canvas floating particle coordinate fields).
3. **Core Utility Mathematics:**
   - `src/utils/easing.ts` (Bézier curves: `cinematic`, `snappy`, `gentle`, `elastic`).
   - `src/utils/textfit.ts` (Dynamic font-size calculation for viewport safety).
4. **Cinematic Rulebook:**
   - `aesthetic-rules.md` (R1-R4, Q1-Q10 from `video-shotcraft`).
   - Sound hierarchy curves and frequency separation guidelines.

---

### 1.2 Adaptation & Refactoring (Enhance Existing Code)

1. **`src/camera/CameraRig.tsx`:**
   - *Current:* Uniform 2D/2.5D scale and tilt.
   - *Adaptation:* Add organic handheld simulation (low-frequency Perlin noise with adjustable amplitude `0.002` to `0.008`), focal depth zoom, and impact impulse shake.
2. **`src/motion/LifeCycle.tsx`:**
   - *Current:* Simple 4-stage lifecycle (`forming`, `resolved`, `handing-off`, `gone`).
   - *Adaptation:* Implement `ambientMode="breathing" | "floating" | "pulsing"` while in `resolved` state, ensuring zero frozen pixels.
3. **`src/theme.ts`:**
   - *Current:* Pure color and spring definitions.
   - *Adaptation:* Add Living Motion physics presets (`viscosity`, `turbulence`, `springRestitution`) and Persian typography scaling tokens.
4. **`scripts/selfcheck.py` & `scripts/motion_check.py`:**
   - *Current:* Checks visual holds and bounding boxes.
   - *Adaptation:* Add checks for Living Motion compliance (reject scenes with zero frame delta between landing and exit) and audio stem alignment.

---

### 1.3 New Implementations (Built Specifically for v2)

1. **Living Motion Engine (`src/living-motion/`):**
   - `NoiseField.ts`: Deterministic procedural Perlin/Simplex noise generator seeded by shot index and frame number.
   - `OrganicBreathing.tsx`: Micro-scale (1.000 -> 1.015) and subtle rotational sway for active hero objects.
   - `SecondaryPhysics.tsx`: Spring-delayed trailing movement for subsidiary elements attached to hero parent transforms.
   - `ParticleDrift.tsx`: Fluid-like ambient drifting dust/micro-elements maintaining deep canvas vitality.
   - `SemanticReaction.tsx`: Audio beat and narration-reactive scale/glow pulses.
2. **Voice Director Subsystem (`audio/` & `scripts/voice_director.py`):**
   - `audio/engine/VoiceEngine.py`: Abstract base provider with adapters for Gemini Cloud TTS, ElevenLabs, Aava Persian TTS, Pocket TTS Farsi, and Edge-TTS.
   - `audio/engine/PersianTextOptimizer.py`: Orthographic & phonetic preprocessor (نیم‌فاصله [ZWNJ], ezafe diacritics, cardinal/ordinal number conversion, Persian calendar conversion, English acronym expansion).
   - `audio/mixer/StemMixer.py`: Automated multi-track stem assembler (`narration.wav`, `music.wav`, `sfx.wav` -> `master_mix.wav`) with dynamic loudness normalization (-16 LUFS) and -14dB narration ducking.
3. **Persian Voice Benchmark Suite (`audio/voice-benchmark/`):**
   - Standalone test suite executing standardized Persian medical/technical test sentences across all providers.
   - Evaluates MOS score, phoneme accuracy, ezafe fidelity, latency, and resource footprint.
