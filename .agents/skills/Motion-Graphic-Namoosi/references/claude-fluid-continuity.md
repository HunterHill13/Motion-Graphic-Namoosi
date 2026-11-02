# Claude Opus 5.5 Fluid Motion & Continuity Reference

## Overview
This reference documents the structural secrets reverse-engineered from viral Claude Opus 5.5 motion graphics (analyzed from primary prompt repositories and live video benchmarks).

---

## 1. The 4 Fluid Continuity Pillars

### Pillar 1: Single Continuous Coordinate World (No Scene Swapping)
* Discrete slideshow scene cuts (`<Sequence from={0} durationInFrames={90}>`) that unmount elements destroy spatial presence.
* In Claude Opus 5.5 videos, all visual actors exist in one persistent 2.5D/3D coordinate space.
* Entities dock, compress, roll, tilt, and transform without ever being unmounted.

### Pillar 2: Motivated 6-DOF Virtual Camera (One-Take Continuity)
* The camera is a continuous cinematic participant executing authored pans, tilts, pitch, roll, and dollys across the entire timeline.
* Transitions between narrative acts are executed via continuous camera maneuvers:
  - Macro focus $\to$ banking roll $\to$ isometric 2.5D tilt $\to$ wide pull-back dolly.
* Strictly forbidden: Random camera shake, decorative 1.05x linear zooms, or abrupt hard cuts.

### Pillar 3: Living Energy Conduit ("The Red Thread")
* A single high-energy focal particle / filament that never leaves the screen.
* Acts as a causal narrative tether:
  - Orbits the hero insignia.
  - Dives into the core to trigger vector morphing.
  - Enters SaaS viewport to paint real-time sparkline graphs.
  - Traverses 3D space to orbit the circular gauge and register completion.

### Pillar 4: Genuine SVG Vector Path Morphing (Not CSS Box Morphing)
* Real SVG `<path>` morphing using `@remotion/paths`'s `interpolatePath(progress, pathA, pathB)`.
* Smooth cubic bezier control-point matching transforms complex geometric shapes into neural matrices, data waves, and verification shields.
* Accompanied by `evolvePath` for mechanical vector stroke reveals (e.g. sovereign checkmarks).

---

## 2. Persian Motion Typography Rules (Yekan Bakh)
1. **Primary Typeface:** `'YekanBakh', 'Yekan Bakh', sans-serif` across 8 weights (100 to 950).
2. **Text Sanitization:** All Persian copy must pass through `sanitizeForDisplay(text)` from `src/typography/persianSanitizer.ts` to eliminate diacritical jitter while preserving institutional orthography.
3. **RTL Flex Ordering:** Layouts must enforce `direction: 'rtl'` with correct horizontal flex reversals (`row-reverse` where needed).
4. **Integer Pixel Coordinates:** Strict rounding (`Math.round()`) and hardware-accelerated transforms to eliminate sub-pixel letterform swimming.
