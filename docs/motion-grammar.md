# Motion Grammar: Semantic Motion Vocabulary for Scientific & Cinematic Visuals (v3.2)

Motion graphics must never move merely because animation is computationally possible. Every animation in the pipeline must communicate explicit narrative and scientific meaning.

---

## 1. Core Semantic Actions & Physical Equivalents

| Biological / Conceptual Action | Motion Metaphor | Physical Implementation | Easing / Curve |
|---|---|---|---|
| **Growth / Expansion** | Outward radial emergence, upward displacement | Scale $0.2 \to 1.05 \to 1.0$, opacity $0 \to 1$ | Spring `damping: 14, stiffness: 110` |
| **Activation / Ignition** | Harmonic luminescence pulse, forward acceleration | Brightness $1.0 \to 2.2 \to 1.0$, bloom expansion | High-frequency sine wave + scale punch |
| **Inhibition / Neutralization**| Sudden deceleration, compression, structural collapse | Kinetic vector stops abruptly, scale shrinks $1.0 \to 0.85$ | Critical damping `damping: 24, mass: 1.2` |
| **Connection / Binding** | Travelling guide spline, convergence to focal node | SVG path stroke-dashoffset draw $\to$ impact latch | Fast ease-in, spring latch settle |
| **Transformation / Morph** | Continuous geometry interpolation, anchor persistence | Path morph, particle coordinate migration | Shared focal anchor, zero canvas reset |
| **Danger / Rupture** | Instability, camera impulse shake, radial fragmentation | Camera shake ($18\text{px}$), shockwave rings | Instant impulse, exponential decay ($8\text{f}$) |
| **Discovery / Reveal** | Camera push-through, aperture widening | Progressive camera tracking $1.0 \to 1.15$, depth defocus | Gentle cubic ease-out |
| **Programmed Death (Apoptosis)**| Symmetric harmonic assembly, radial pulse propagation | Heptameric gear spoke rotation, cascading waves | Constant rotational velocity + pulse wave |

---

## 2. Motion Hierarchy per Shot

1. **Primary Motion (Narrative Lead):** The hero molecule or organelle executing the visual sentence (e.g. BH3 peptide projectile flight).
2. **Secondary Motion (Reaction):** Elements physically attached or responding to the hero (e.g. membrane deformation, reticle tracking).
3. **Ambient Motion (Continuous Life):** Brownian particle drift, subtle fluid mesh deformation ($1.000 \to 1.018$ scale breathing) to prevent screen freezing.
4. **Micro Motion:** High-frequency optical shimmer and glow fluctuation during hold sections.
