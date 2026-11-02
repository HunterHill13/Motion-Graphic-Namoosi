# MOTION GRAMMAR: SEMANTIC ANIMATION RULES

## The Prime Rule
> **NEVER ANIMATE AN ELEMENT WITHOUT A REASON.**
> Motion is not decoration; motion is semantic punctuation.

## The Semantic Dictionary

| Narrative Concept | Animation Mechanism | Implementation Example |
|---|---|---|
| **Growth / Expansion** | Progressive Scale + Radial Push | `scale(0.85 -> 1.0)` with smooth spring overshoot |
| **Causality / Transmission** | Directional Vector Travel | Connecting line drawn via `strokeDashoffset`, followed by target pop |
| **Comparison / Contrast** | Split Screen / Opposing Vectors | Elements slide from left and right into dual cards |
| **Significance / Importance** | Hero Glitch + Rim Glow + Radial Wash | `StageLine` flash + `HeroGlow` activation |
| **Yielding / Hand-off** | Downscale + Dim + Defocus | `<Live demoteAt={t}>` (scale 0.92, opacity 0.35, blur 3px) |
| **Irreversible Reaction** | High-energy Particle Burst / Shatter | Instant pore opening, particles emitting outward |
| **Convergence / Synthesis** | Multi-vector Inward Assembly | All features fly in from 4 quadrants into the finale family card |
| **Focus / Inspection** | Camera Push + Peripheral Dimming | CameraRig scales 1.00 -> 1.05 while non-target elements fade |
