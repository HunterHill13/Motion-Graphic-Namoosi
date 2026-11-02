# LIVING MOTION ENGINE SPECIFICATION (v2)

**Document:** `docs/LIVING_MOTION.md`  
**Target:** Elimination of Static Presentation Look & Infusion of Organic Physicality  
**Date:** 2026-10-04  

---

## 1. Principles of Living Motion

Conventional AI-generated motion graphics look like animated slide decks because elements animate in, freeze completely while the voice speaks, and then abruptly animate out.

The **Living Motion Engine** enforces four core tenets:
1. **Continuous Vitality:** Every on-screen element has an idle lifecycle state characterized by sub-perceptual organic motion.
2. **Deterministic Procedural Noise:** Randomness must be seed-deterministic and frame-driven (`f(frame, seed)`) so renders are 100% reproducible across frames and concurrency threads.
3. **Physical Hierarchy & Inertia:** Secondary visual elements (badges, connectors, annotations) must lag behind parent elements with realistic spring elasticity.
4. **Narration-Reactive Vitality:** Visual intensity subtly swells in sympathy with acoustic emphasis.

---

## 2. Mathematical Formulations

### 2.1 Low-Frequency Organic Noise (Drift & Sway)
To simulate natural handheld camera drift or biological fluid movement without high-frequency jitter:
$$\text{Noise}(t, \text{seed}) = \sum_{i=1}^{k} A_i \cdot \sin(2\pi \cdot f_i \cdot t + \phi_i(\text{seed}))$$
Where:
- $k = 3$ (Three octaves of sinusoids with irrational frequency ratios to avoid visible periodicity).
- $f_1 = 0.15\,\text{Hz},\; f_2 = 0.37\,\text{Hz},\; f_3 = 0.81\,\text{Hz}$.
- $A_1 = 0.60,\; A_2 = 0.28,\; A_3 = 0.12$.

### 2.2 Micro-Breathing Function
Hero elements oscillate slightly in scale and glow during their active `resolved` lifecycle phase:
$$S(t) = 1.000 + A_{\text{breathe}} \cdot \sin\left(\frac{2\pi \cdot t}{T_{\text{breathe}}}\right)$$
- $A_{\text{breathe}} \in [0.008, 0.015]$ (Subtle $0.8\% - 1.5\%$ expansion).
- $T_{\text{breathe}} \in [90, 150]\,\text{frames}$ ($3.0 - 5.0\,\text{seconds}$ at $30\,\text{fps}$).

### 2.3 Secondary Elastic Inertia (Trailing Spring Lag)
For an attached badge or annotation following a parent coordinate $X_{\text{parent}}(t)$:
$$X_{\text{child}}(t) = X_{\text{parent}}(t - \Delta) + \text{spring}\left(\text{stiffness}=100, \text{damping}=18\right)$$
Where $\Delta \in [4, 8]\,\text{frames}$, creating a natural organic follow-through.

---

## 3. The v2 8-Layer Shot Architecture (L0 - L7)

1. **L0: Canvas Grid & Coordinate Substrate:** Subtle mathematical grid, deep coordinate ticks, or spatial perspective guides.
2. **L1: Camera:** Dynamic `LivingCameraRig` combining cinematic push/pull (1.00 -> 1.05) with low-frequency handheld procedural drift and impact damping.
3. **L2: Optical Focus & Volumetrics:** Depth-of-field blur, atmospheric haze, lighting sweeps, and volumetric dust particles.
4. **L3: Primary Hero Subject:** Central semantic model, diagram, or anatomical structure with micro-breathing and deformation.
5. **L4: Attached Secondary FX:** Halo rings, biological membranes, energy pulses, and light sheens anchored to the hero.
6. **L5: Secondary Information & Connectors:** Dynamic callout lines, labels, telemetry badges, and comparative nodes with spring lag.
7. **L6: Deep Environment:** Procedural star fields, dot matrices, floating micro-particles, and subtle radial gradient mesh.
8. **L7: Master Overlays & Film Treatment:** Procedural SVG film grain, color grading LUT, progress tracking, and accessible subtitles.

---

## 4. Component Implementations to Create in `src/living-motion/`

- `NoiseField.ts`: Frame-based deterministic multi-octave 1D/2D noise helper.
- `OrganicBreathing.tsx`: React wrapper applying micro-scale and breathing luminance.
- `LivingCameraRig.tsx`: Drop-in replacement for `CameraRig.tsx` with organic drift and impulse shake.
- `SecondaryPhysics.tsx`: Container delaying and softening child motion relative to parent.
- `ParticleDrift.tsx`: Lightweight canvas particle system with Brownian motion and depth sorting.
- `SemanticPulse.tsx`: Keyframe-driven expansion and glow tied to audio beat timings.
