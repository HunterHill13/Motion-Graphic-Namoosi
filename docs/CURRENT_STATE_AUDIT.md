# CURRENT STATE AUDIT: CINEMATIC MOTION-GRAPHICS AGENT (v1 -> v2)

**Audit Date:** 2026-10-04  
**Auditor:** Senior AI Video Pipeline Architect & Lead Agent Engineer  
**Repository:** `HunterHill13/Cinematic-Motion-Graphics-Agent-Skill-Plan`  
**Current Git Commit:** `729add3` (Clean working tree on `main`)

---

## 1. Executive Summary

The v1 release established a rock-solid, production-tested foundation for AI-directed cinematic motion graphics. It introduced the canonical **7-layer shot model**, **Pilot Gate**, **Dual-Tier QC**, **Antigravity Skill packaging**, and **CameraRig subtle dynamics**.

However, to elevate this system into a genuinely world-class film-production engine (v2), we must address critical architectural gaps:
1. **Motion Staticness:** The current system relies on simple entrance/exit springs and linear camera scale. Elements remain rigid and mechanical after entrance; there is no organic non-repetitive micro-noise, secondary fluid physics, or element-level ambient breathing.
2. **Audio Architecture:** Voice synthesis is currently treated as an auxiliary script (`scripts/tts_build.py`) with no provider abstraction, stem separation, ducking, or musical beat synchronization.
3. **Persian Voice Support:** Microsoft/Azure TTS produces robotic, artificial Persian intonation. There is no benchmark suite, no phonetic/orthographic Persian text optimizer (نیم‌فاصله, ezafe, number expansion, English loanword normalization), and no pluggable support for modern neural Persian engines (Gemini TTS, ElevenLabs, Aava TTS, Pocket TTS Farsi).

---

## 2. Inventory: Implemented vs. Partial vs. Missing

| Subsystem / Capability | Current Status in v1 | Detail & Evidence | v2 Upgrade Requirement |
|---|---|---|---|
| **Antigravity Skill Spec** | **Fully Implemented** | `.agents/skills/cinematic-motion-director/SKILL.md` (205 lines), 12 references, 5 JSON schemas, 6 templates, 5 mode workflows. | Extend skill with Voice Director, Living Motion, and Persian TTS specifications. |
| **7-Layer Shot Model** | **Fully Implemented** | L1 Camera, L2 Focus, L3 Subject, L4 FX, L5 Secondary, L6 Env, L7 Overlays documented and tested. | Introduce L0 Canvas Grid & deeper layer interaction. |
| **CameraRig System** | **Fully Implemented** | `src/camera/CameraRig.tsx` continuous scale (1.00 -> 1.05) + 2.5D tilt. | Add procedural camera drift (Perlin-style low-frequency noise), dynamic focal depth, and shake impulses. |
| **State Machine (`demoteAt`)** | **Fully Implemented** | `src/motion/LifeCycle.tsx` handles forming -> resolved -> handing-off -> gone. | Add continuous micro-breathing during the `resolved` state. |
| **Theme & Design Tokens** | **Fully Implemented** | `src/theme.ts` with 4 palette presets (`medicalBio`, `darkTech`, `warmEditorial`, `warmPremium`), 60/30/10 rule. | Expand with living motion frequencies, organic noise parameters, and Persian typography scale. |
| **Two-Tier QC Pipeline** | **Fully Implemented** | `scripts/motion_check.py`, `scripts/frame_metrics.py`, `scripts/selfcheck.py`, pilot gate logs. | Add audio/stem QC (`scripts/audio_qc.py`), Living Motion noise verification, and Persian pronunciation sanity check. |
| **Living Motion Engine** | **Missing / Barebones** | Only basic CSS animations and Remotion springs exist. | **NEW:** Create `src/living-motion/` (procedural noise, spring physics, ambient breathing, particle drift, organic deformation, semantic reaction). |
| **Voice Director Subsystem** | **Missing** | Script-to-audio is manual and uncoordinated. | **NEW:** Create `audio/` structure with `VoiceEngine` abstraction, stem separation (`narration/`, `music/`, `sfx/`, `mixed/`), and automatic ducking. |
| **Persian TTS & Benchmark** | **Missing** | Only generic Edge-TTS is configured. | **NEW:** Create `scripts/persian_text_norm.py`, `scripts/voice_director.py`, and `audio/voice-benchmark/` comparing Gemini TTS, ElevenLabs, Aava TTS, Pocket TTS Farsi, and local models. |

---

## 3. What Can Be Reused Without Modification

1. **Remotion Core Engine & Project Setup:**
   - `package.json`, `tsconfig.json`, `remotion.config.ts`, `src/index.ts`, `src/Root.tsx`.
   - Remotion official skills integration (`remotion-best-practices`, `remotion-render`, `remotion-studio`).
2. **Foundational Effects & Overlays:**
   - `src/effects/Grain.tsx`, `src/effects/Grade.tsx`, `src/effects/BgMesh.tsx`, `src/effects/Vignette.tsx`, `src/effects/DotFieldBg.tsx`, `src/effects/StarFieldBg.tsx`.
   - `src/overlays/ProgressBar.tsx`, `src/captions/Subtitle.tsx`.
3. **Math & Easing Utilities:**
   - `src/utils/easing.ts`, `src/utils/textfit.ts`, `src/utils/timeline.ts`, `src/utils/types.ts`.
4. **Research & Factual Grounding Framework:**
   - `research/sources.md`, `research/research.md`, medical claim citation contracts.
5. **Pilot Gate Workflow:**
   - First 10–30s inspection rule, QC checklists (`qc/pilot.md`, `qc/final.md`).

---

## 4. What Must Be Refactored or Extended

1. **`src/camera/CameraRig.tsx`:**
   - *Current:* Linear or single-spring push/pull (`scale: 1.00 -> 1.05`).
   - *Upgrade:* Integrate multi-octave procedural drift, Dutch tilt micro-sway, and cinematic impulse damping.
2. **`src/motion/LifeCycle.tsx`:**
   - *Current:* Static between entrance and exit.
   - *Upgrade:* Integrate ambient idle oscillation so elements stay alive without distracting from new heroes.
3. **`scripts/tts_build.py`:**
   - *Current:* Monolithic script tightly coupled to edge-tts.
   - *Upgrade:* Refactor into a modular `VoiceDirector` provider pipeline (`audio/engine/`) supporting multiple TTS backends, Persian normalization, and frame-accurate word boundary manifests.
4. **`.agents/skills/cinematic-motion-director/SKILL.md`:**
   - *Upgrade:* Expand system prompt and references to mandate Living Motion compliance, Voice Director timing protocols, and Natural Persian voice workflows.

---

## 5. What Must NOT Be Touched

- **Do NOT break the 5 Input Modes contract** (Mode A through Mode E).
- **Do NOT weaken the Pilot Gate** (First 10–30s inspect-before-render constraint).
- **Do NOT degrade render performance** or introduce browser DOM hacks; keep all canvas/CSS transforms seek-safe and deterministic.
- **Do NOT hardcode external proprietary API keys** in codebase; use clean environment variables and local offline fallbacks.
