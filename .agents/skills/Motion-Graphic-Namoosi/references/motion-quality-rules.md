# MOTION QUALITY RULES & THE 5-LAYER STACK

Adapted from `claude-remotion-skill` and production battle-testing.

## 1. The 13 Motion Quality Laws
1. **Zero Linear Easing**: Never use linear interpolation for spatial movement or scale. Always use Remotion `spring()` or clamped cubic bezier curves.
2. **Multi-Property Entrances**: Single-property fades look cheap. Every entrance must combine at least two properties (e.g. `opacity` + `translateY` + `scale`).
3. **Staggered Choreography**: Offset sibling elements by 3–6 frames. Nothing enters at the exact same instant.
4. **Faster Exits**: Exits must be snappy (8–14 frames), clearing the frame faster than entrances (18–25 frames).
5. **Holds are Design Tools**: Rapid movement $\to$ complete stillness $\to$ next move. Constant motion reads like amateur jitter; stillness creates contrast and legibility.
6. **Frame-Based Math**: Every animation value is computed strictly from `useCurrentFrame()` and `useVideoConfig().fps`. Zero `setTimeout` or wall-clock dependencies.
7. **No Magic Numbers**: Interpolation domains and ranges must be computed from duration tokens or layout constants.
8. **Ken Burns on All Stills**: If a static image is displayed, apply a subtle scale drift ($1.00 \to 1.04$) to maintain optical life.
9. **No Dead Backgrounds**: Use `BgMesh` or subtle procedural particles; never pitch-black single-color voids.
10. **The 60/30/10 Color Rule**: 60% base tone, 30% surfaces/borders, 10% hero color. Maximum ONE glowing or hero-colored focal element per frame.
11. **Sound Sync Offset**: Sound effects must start 2–3 frames BEFORE visual impact to match human audiovisual sensory integration.
12. **Safe Margins**: Keep all critical text within 12% vertical and 8% horizontal margins.
13. **Mandatory Render Inspection**: Every render must be extracted to frame stills and visually checked before approval.

## 2. The Universal 5-Layer Stack
Every composition must assemble the following 5 layers:
```text
Layer 5: Procedural Film Grain (SVG Turbulence, 0.04 opacity, overlay)
Layer 4: Vignette (Radial gradient lens falloff)
Layer 3: Color Grade Overlay (Soft-light tint unifying assets)
Layer 2: CameraRig & Active Scene Content (Heroes, text, cards, transitions)
Layer 1: Ambient Background (BgMesh / DotFieldBg / StarFieldBg)
```
