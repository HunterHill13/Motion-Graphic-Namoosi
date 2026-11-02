# Builder Protocol & Remotion Engineering Standards

## Mandate: Clean Code, Zero Ad-Hoc Drift, Strict Catalog Reuse

The Builder role translates an approved **Director Shot Plan** into high-performance, deterministic Remotion code (`src/shots/*.tsx`, `src/scenes/*.tsx`).

---

## 1. Operating Rules for the Builder

1. **Search Before Authoring**:
   - Check `V18_MOTION_CATALOG.md` and `src/motion/recipes/` before writing any new animation logic.
   - Compose existing primitives (`TypographySlam`, `TextMaskReveal`, `DotToLine`, `RibbonGrowth`, `ShapeMorph`, `SequentialSwap`) instead of inventing inline transforms.

2. **Strict Content Locking**:
   - The Builder may invent visual form, geometry, masks, timing curves, and camera motion.
   - The Builder may **NEVER** alter spoken voiceover words or display text approved in the Director Shot Plan.

3. **Remotion Invariants (Avoid Known Traps)**:
   - **Clamping**: Always pass `{ extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }` to frame-based `interpolate()`.
   - **Spring Unclamped**: When mapping `spring()` progress to spatial properties, leave output unclamped to preserve natural physical overshoot.
   - **No Inline Transform Bug**: Always use `display: 'inline-block'` on typography spans receiving transforms; raw `<span>` tags silently ignore CSS `transform`.
   - **Alpha Transparency**: Never add a `backgroundColor` to root `<AbsoluteFill>` when rendering transparent graphic overlays.
   - **ClipPath over Scale**: Use `clipPath: inset(...)` for reveal panels with text; never use `scaleX` or `scaleY` which distort font letterforms.
   - **Tabular Numbers**: Always attach `fontVariantNumeric: 'tabular-nums'` to animated statistical counters.
   - **No Hooks in Loops**: Never call `spring()` or `useCurrentFrame()` inside `.map()`; extract dedicated child components.

4. **Sequential Swap Rule**:
   - Outgoing elements must be completely exited before incoming elements begin their arrival.
   - Maximum overlap permitted is 1 frame with outgoing element $\ge 95\%$ transparent.

5. **Visual Hit Leading**:
   - For any motion event aligned to a spoken beat or SFX hit, initiate the entrance 2–4 frames *before* the acoustic peak (`spHit` pattern) so the eye registers the visual impact synchronously with the sound.
