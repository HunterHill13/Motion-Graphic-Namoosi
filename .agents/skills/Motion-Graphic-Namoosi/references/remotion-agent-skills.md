# Remotion Agent Skills Doctrine (Official Best Practices)

Adapted from `remotion-dev/skills` (`@remotion/skills` v4.0):

## 1. Frame-Driven Animation Principles
- Inside any composition, read `fps` from `useVideoConfig()`.
- Use `useCurrentFrame()` and `interpolate()` as the absolute source of truth.
- **Strict Ban on CSS Transitions / Keyframe Animations:** Headless rendering scrubs frames deterministically. CSS `transition` or `animation` classes will fail or drop frames during export.

## 2. Spring Physics Standard
Always prefer `spring()` or `Easing.spring()` over bouncy cubic-bezier curves:
```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const entrance = spring({
  frame,
  fps,
  config: {
    damping: 14, // 12-18 provides snappy settle with subtle overshoot
    mass: 0.8,
    stiffness: 120, // 100-150 creates responsive, modern motion
  },
});
```

## 3. CSS Transform Shorthands
In React/Remotion inline styles, use individual CSS properties (`scale`, `translate`, `rotate`) rather than monolithic `transform` strings. This ensures subpixel accuracy and enables the Remotion Studio UI to inspect and manipulate individual axes.

```tsx
// RECOMMENDED:
style={{
  scale: interpolate(frame, [0, 20], [0.8, 1], { extrapolateRight: 'clamp' }),
  translate: `0px ${interpolate(frame, [0, 20], [40, 0], { extrapolateRight: 'clamp' })}px`,
  opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
}}
```

## 4. Sequence-Local Timing & Premounting
- **Sequence Context:** A component nested inside `<Sequence from={N}>` receives `useCurrentFrame()` starting at 0. Always calculate delays relative to the sequence start (`delayFrames={4}`), never global timeline timestamps.
- **Premounting:** For heavy media or nested sequences, supply `premountFor={fps}` to pre-render visual assets and eliminate initial frame drop.
