# Component Recipes & Motion Primitives

This reference catalogs the modular Remotion React components in `src/motion/library/`, `src/motion/recipes/`, and `src/typography/`.

---

## 1. Persian Kinetic Typography (`PersianKineticText`)
- **Location:** `src/typography/PersianKineticText.tsx`
- **Purpose:** Word-level staggered kinetic entrance protecting Persian cursive ligatures.
- **Modes:**
  - `curtain` (Default): Baseline clip-path curtain reveal (`clipPath: inset(0 0 progress% 0)`).
  - `flip3d`: Mechanical 3D perspective flip (`rotateX(-80deg -> 0deg)`).
  - `pop`: Scale arrival (`scale(0.85 -> 1.0)`) with opacity spring.
  - `skew`: Horizontal velocity slide (`translateX(±120px -> 0)` with `skewX(-14deg -> 0)`).
- **Physics Contract:** Uses `SPRING_PRESETS.TYPOGRAPHY_WORD_STAGGER` ($\zeta=0.90$, `overshootClamping: true`).

---

## 2. Dynamic Vector Morphing Card (`PersianVectorMorphCard`)
- **Location:** `src/motion/library/PersianVectorMorphCard.tsx`
- **Purpose:** Smooth cubic bezier morphing between distinct vector path topologies via `@remotion/paths`'s `interpolatePath(progress, pathA, pathB)`.
- **Key Path Presets:** `NEURAL_SYNAPSE`, `DNA_HELIX_ORBIT`, `QUANTUM_ORBITALS`, `EXPONENTIAL_CHART`, `SECURITY_SHIELD`, `STELLAR_OCTAGRAM`, `CIRCUIT_CHIP`.

---

## 3. Atmospheric Backdrop & Volumetric Lighting
- **Location:** `src/motion/library/StudioMeshGlassBackdrop.tsx` & `AtmosphericBackdrop.tsx`
- **Purpose:** Multi-layer volumetric radial lighting with native `in oklch` color space interpolation.
- **Performance Budget:** Maximum 2 simultaneous blur/filter layers active at any given frame.

---

## 4. Topic-Specific Scientific Motifs
- **Newtonian Attractor Swarm (`NewtonianAttractorSwarm.tsx`):**
  - Deterministic gravitational particle orbits (15–18 particles) around focal cores.
  - Deployed exclusively on AI, biotech, and deep science topics; omitted on corporate, paper, and minimal layouts.
- **Lissajous Orbit (`ProceduralGenerativeMotifs.tsx`):**
  - Multi-frequency trigonometric knot ($x = A\sin(a\theta + \delta), y = B\sin(b\theta)$) for physics and data signals.

---

## 5. Kinetic Data Visualization (`KineticDataViz.tsx`)
- **Location:** `src/motion/library/KineticDataViz.tsx`
- **Components:**
  - `KineticMetricCounter`: Integer and decimal count-up interpolations.
  - `KineticRadialProgress`: Circular progress gauges with reactive glow heads.
  - `BarChartVisualizer`: Spring-loaded comparative horizontal bars.

---

## 6. Studio Anticipation Spring & Volume Preservation
- **Location:** `src/motion/physics/SpringPhysicsMatrix.ts`
- **Anticipation (`studioAnticipationSpring`):**
  - Executes a 3–5f negative recoil dip ($2\% \text{ to } 6\%$) before explosive spring release.
  - Eliminates robotic start from dead stop.
- **Volume Preservation (`calculateSquashAndStretch`):**
  - Maintains $S_x \cdot S_y \cdot S_z = 1.0$ during impacts and velocity peaks.
  - Prevents isotropic balloon inflation during landing.

---

## 7. Voice-Synchronized Progressive Semantic Highlighting
- **Location:** `src/typography/PersianKineticText.tsx`
- **Purpose:** Spoken keywords illuminate dynamically with radiant glow (`textShadow`) and subtle scale bump ($1.05$) during voiceover milestones.
- **Contract:** Zero horizontal margin alteration to protect Persian cursive ligatures.

---

## 8. Decoupled Camera Crane Rig & Velocity Motion Blur
- **Location:** `src/motion/camera/UniversalCameraRig.ts`
- **Subpixel Flight:** Uses floating-point `.toFixed(2)` coordinates inside `preserve-3d` wrapper to eliminate 1px staircase judder on 4K/retina displays.
- **Active Motion Blur:** Injects directional SVG/CSS blur during velocity peaks ($\|v\| > 15\text{px/frame}$).
- **Crane Dynamics:** Centrifugal roll banking $\text{Roll} \propto -\frac{d^2 X}{dt^2}$ and boom pitch inertia $\text{Pitch} \propto \frac{d^2 Y}{dt^2}$.

