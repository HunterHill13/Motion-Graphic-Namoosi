# Consolidated Architecture Specification (v40.1)

## 1. System Overview & Clean Separation of Concerns
The Cinematic Motion Director system strictly isolates three functional boundaries:
1. **The Reusable Skill (`.agents/skills/cinematic-motion-director/`):** The general, project-agnostic directing and production intelligence. Governs causal graphs, element budgeting, authored keyframes, camera grammar, audio ducking standards, and quality release gates.
2. **The Core Production Library (`src/`):** The shared React and Remotion components, mathematical motion engines (`src/motion/`), camera rigs (`src/camera/`), typography systems (`src/typography/`), and transition handlers (`src/transition/`).
3. **The Project Workspace (`projects/band-kaf/`):** Project-specific narrative assets, scripts, audio recordings, custom 3D art direction, and storyboard specifications.

---

## 2. End-to-End Production Pipeline Architecture

```text
               REUSABLE SKILL (cinematic-motion-director)
                                   ↓
                       DIRECTOR: SEMANTIC INTAKE
      (Script Analysis, ASR Word Timestamps, Semantic Beat Mapping)
                                   ↓
                                SHOTBOOK
     (docs/SHOTBOOK.md: 1 Primary Visual Job per Beat, Timing Windows)
                                   ↓
                           CAUSAL EVENT GRAPH
  (references/causal-planning.md: State -> Anticipation -> Cause -> Action -> Settle)
                                   ↓
                        ELEMENT BUDGETING & LAYOUT
      (Max 1 Primary Hero, 1-2 Secondary, 0-2 Tertiary, >= 1 Empty Quadrant)
                                   ↓
                    CORE MOTION & TRANSFORMATION ENGINES
 (AuthoredKeyframeEngine, PhysicalBounceRecipe, TransformationContinuityEngine)
                                   ↓
                       CINEMATIC CAMERA GRAMMAR
    (CameraGrammarRig: Motivated moves only, Seismic Shock, Zero Idle Jitter)
                                   ↓
                      AUDIO & PROSODY INTEGRATION
   (Google Gemini TTS `Puck`, Dual-Script Sanitizer, -14dB Sidechain Ducking)
                                   ↓
=========================== PROJECT BOUNDARY ===========================
                                   ↓
                   PROJECT-SPECIFIC COMPOSITIONS
   (e.g., Sovereign Calibration Pavilion & Kinetic Monolith in `projects/band-kaf/`)
                                   ↓
                     13 AUTOMATED RELEASE GATES
 (Frame Metrics, Causal Audits, Audio Loudness, Anti-Pattern Review, Zero Lint)
                                   ↓
                       FINAL MASTER RENDER (Remotion)
            (renders/v40/V40.1_PREVIEW_KINETIC_MONOLITH.mp4)
```

---

## 3. Directory Layout & Boundaries

```text
.
├── .agents/skills/cinematic-motion-director/  # REUSABLE AGENT SKILL (Project-Agnostic)
│   ├── SKILL.md                              # Master Directing Directive
│   ├── references/                           # Architectural Standards
│   │   ├── causal-planning.md                # Causal Event Graphs & Budgeting
│   │   ├── living-motion.md                  # Organic Motion & Authored Curves
│   │   ├── voice-director-and-persian-tts.md # Gemini TTS Protocol & Audio Ducking
│   │   ├── camera-director.md                # Cinematic 3D Camera Choreography
│   │   ├── remotion-core-engine.md           # Remotion React Engine Standards
│   │   └── anti-patterns.md                  # Catalog of Historical Failures
│   └── template/                             # Clean scaffolding for fresh projects
│
├── src/                                      # PRODUCTION CODEBASE
│   ├── production/                           # Production Entrypoints
│   │   └── BandKafPreviewComposition.tsx     # Active Flagship Composition Export
│   ├── motion/                               # Mathematical Motion Engines
│   │   ├── curves/                           # AuthoredKeyframeEngine (bezier profiles)
│   │   ├── physics/                          # PhysicalBounceRecipe (parabolic, COR)
│   │   ├── fidelity/                         # MotionFidelityEngine (8 personalities)
│   │   ├── recipes/                          # Reusable animation building blocks
│   │   └── TransformationContinuityEngine.ts # 2D->3D & Volume Conservation
│   ├── camera/                               # CameraGrammarRig & CameraRig
│   ├── typography/                           # Zero-Subpixel Persian typography & Sanitizer
│   ├── transition/                           # Motion-Carry Transitions
│   ├── choreography/                         # ChoreographyEventGraph Engine
│   ├── Root.tsx                              # Minimal, clean Remotion registry
│   └── Main.tsx                              # Modular 6-shot film template
│
├── projects/                                 # PROJECT WORKSPACES
│   └── band-kaf/                             # Standalone Band Kaf Project
│       ├── script/                           # Phonetic & Display scripts
│       ├── audio/                            # Gemini TTS WAVs, MP3 master, Python mix
│       ├── compositions/                     # BandKafMonolithPreview
│       ├── renders/                          # Video exports and audit stills
│       └── project-notes/                    # Art direction, causality maps, plans
│
├── archive/                                  # HISTORICAL R&D (V1 - V39)
│   ├── README.md                             # Version registry and lessons learned
│   ├── legacy_projects/                      # Archived test suites (v3 to v19)
│   ├── legacy_labs/                          # Archived precision labs (v27 to v38)
│   └── experiments/                          # Failed experiments (e.g. v39 slideshow)
│
├── docs/                                     # ARCHITECTURAL DOCUMENTATION
│   ├── CAPABILITY_INVENTORY.md               # Historical capability audit
│   ├── CAPABILITY_CONSOLIDATION_MATRIX.md    # Consolidation decisions
│   ├── ARCHITECTURE.md                       # This document (Single Source of Truth)
│   ├── PRODUCTION_CONTRACT.md                # Acceptance criteria for future videos
│   └── CONSOLIDATION_REPORT.md               # Final consolidation report
│
└── renders/                                  # Global build exports
```

---

## 4. Subsystem Specifications

### 4.1 Motion & Transformation Engine
- **AuthoredKeyframeEngine:** Evaluates multi-phase piecewise bezier curves (`evaluateAuthoredKeyframeTrack`). Keyframe roles (`REST`, `ANTICIPATION`, `LAUNCH`, `PEAK`, `IMPACT`, `OVERSHOOT`, `SETTLE`) provide micro-frame directorial control over speed and force.
- **Continuous 2D $\to$ 3D:** Vector SVGs preserve topological slice integrity, rotating into orthographic and perspective depth using CSS 3D transforms without Three.js overhead.
- **Mass & Volume Conservation:** All squashing or impact deformations maintain physical mass volume:
  $$\text{scaleX} \cdot \text{scaleY} = 1.0$$

### 4.2 Camera Grammar
- **Motivated Motion Only:** Camera moves are tied directly to narrative scope. A crane pull-back is used when the scope broadens (e.g. revealing the full trilogy); an orbital push-in occurs during high-stakes focus.
- **Seismic Shock Reaction:** When an entity strikes the ground with mass, the camera executes a 3-frame vertical kick ($+8\text{px} \to -4\text{px} \to 0\text{px}$).
- **Intentional Stillness:** Continuous camera breathing or idle sinusoidal floating is strictly banned.

### 4.3 Typography & Dual-Script Architecture
- **SpeechText (Phonetic):** Carries Arabic/Persian diacritics (harakat/tashdid) required to prevent Google Gemini TTS from mispronouncing scientific or institutional terms.
- **DisplayText (Visual):** Processed via `src/typography/persianSanitizer.ts`, stripping all diacritics and normalizing zero-width non-joiners for clean visual typography.
- **Subpixel Locking:** Integer coordinates (`Math.round`), `translate3d(0,0,0)`, and `backface-visibility: hidden` prevent blur and text vibration during animation.

### 4.4 Audio Mastering
- **Gemini TTS Mandate:** Exclusively uses Google Gemini Multimodal Audio API (`gemini-2.5-flash-preview-tts` with voice `Puck`).
- **Dynamic Ducking:** Music ducks by -14 dB under voiceover using FFmpeg `sidechaincompress` (200ms attack, 800ms release) and normalized to EBU R128 (-16 LUFS).
