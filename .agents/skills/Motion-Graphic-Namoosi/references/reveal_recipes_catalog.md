# Kinetic Typography & Reveal Recipes Catalog

> Production-tested kinetic recipes synthesized from `iart-ai/kinetic-typography-skills` and adapted for high-density broadcast Remotion compositions.

---

## 1. Core Kinetic Principles

1. **Text as a Physical Actor:** Text is not an administrative label; it is a physical entity with mass, momentum, and architectural presence.
2. **Word-Level Chunking:** Never reveal full sentences at once. Group words into natural semantic chunks ($2-4$ words) synchronized with speech prosody.
3. **Zero Ligature Fragmentation:** In Persian/Arabic scripts, character-by-character splitting (`text.split('')`) destroys connected cursive forms and is strictly banned. Only word-level or phrase-level splitting is permitted.

---

## 2. Master Reveal Recipes

### Recipe 1: Masked Directional Wipe (`clipPath` Reveal)
* **Visual Feel:** Text rises out of an invisible razor-sharp horizon line with high momentum.
* **Remotion Implementation:**
  ```tsx
  // Wrapper container with vertical clearance for Persian diacritics
  <div style={{ overflow: 'hidden', padding: '10px 0' }}>
    <div style={{
      transform: `translateY(${interpolate(springProgress, [0, 1], [120, 0])}%)`,
      opacity: interpolate(springProgress, [0, 0.3], [0, 1])
    }}>
      {phrase}
    </div>
  </div>
  ```
* **Physics Preset:** `SpringPhysicsMatrix.TYPOGRAPHY_WORD_STAGGER` (damping $\ge 0.90$, clamp: true).

### Recipe 2: The Scale-Settle Arrival
* **Visual Feel:** Element arrives with explosive energy, landing slightly oversized before snapping crisply into resting scale.
* **Remotion Implementation:**
  ```tsx
  const scale = interpolate(springVal, [0, 1], [1.14, 1.00]);
  const opacity = interpolate(springVal, [0, 0.2], [0, 1]);
  ```
* **Physics Preset:** `SpringPhysicsMatrix.STATUS_BADGE_PILL` (stiffness 160, damping 12).

### Recipe 3: The Mechanical Split-Flap Counter
* **Visual Feel:** Airport terminal departure board ticking rapidly before arresting on the target number.
* **Remotion Implementation:**
  - Fast vertical drum rotation around the $X$-axis (`rotateX`) with `backfaceVisibility: hidden`.
  - Incremental numeral progression tied to frame count, settling with a 2-frame bounce on the final value.

### Recipe 4: Monumental Headline Slam
* **Visual Feel:** Heavy structural masonry arrival where massive text impacts the canvas, transferring momentum into camera screen-shake.
* **Remotion Implementation:**
  - Massive font size ($160\text{px} - 240\text{px}$), weight 900.
  - Scale lands from $2.2\times \rightarrow 1.0\times$ in 6 frames.
  - On frame of impact, trigger a 3-frame camera shake ($dX = \pm 12\text{px}$, $dY = \pm 8\text{px}$) that dampens immediately.

---

## 3. Typographic Avoidance Contracts

- **Banned:** Character-level cursive splitting in Persian.
- **Banned:** Long subtitle paragraphs at the bottom of the screen.
- **Banned:** Unrounded subpixel coordinates ($X, Y$) on settled text causing rasterizer shimmer.
- **Banned:** Using CSS `@keyframes` instead of Remotion frame-driven springs.
