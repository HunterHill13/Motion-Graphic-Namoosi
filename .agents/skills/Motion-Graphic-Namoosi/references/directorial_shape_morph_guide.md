# Directorial Guide: Shape Morph (`08-morph`)
## Canonical Metaphoric Morph Chain Engine

* **Style Slug:** `08-morph`
* **Benchmark Reference:** Upstream Style 06 (Morphe / Apple Keynote / Pentagram)
* **Default Rhythm:** 150 BPM (1 beat = 0.40s = 12 frames at 30 FPS)
* **Standard Duration:** 10.00 seconds (300 frames)

---

## 1. Directorial Narrative Doctrine

Shape Morph is the art of **continuous conceptual metamorphosis**. A single hero silhouette transitions continuously across 6 to 8 thematic metaphors on the musical beat, conveying narrative transformation without cuts, dissolves, or camera repositions.

```
Drop ──► Coffee Cup ──► Sun ──► Sunset ──► Gull ──► Supersonic Plane ──► Map Pin ──► Pulsing Heart ──► Wordmark
```

### Prohibited Anti-Patterns (Automatic Failures)
* **Direct Complex-to-Complex Morphing (`DIRECT_SHAPE_MORPH_DEFECT`):** Interpolating directly between two topologically complex polygons without collapsing through an intermediate neutral primitive. This causes chaotic edge crossings and tangled vector knots.
* **Non-Continuous Cuts:** Crossfading or cutting to black between morph targets.
* **RGB Color Desaturation:** Blending background wipe colors in standard sRGB or HSL, creating muddy, desaturated brownish midpoints.

---

## 2. The Two-Phase Intermediate Collapse Requirement

To guarantee mathematically pure, visually elegant transitions, **every transformation must pass through an intermediate neutral primitive**:

```
Shape A (Complex) ──► Phase 1: Collapse (8-12f) ──► Neutral Primitive (Circle/Capsule) ──► Phase 2: Bloom (8-12f) ──► Shape B (Complex)
```

1. **Phase 1: Intermediate Collapse (8 to 12 frames):**
   - The perimeter vertices of Shape $A$ contract toward its arithmetic centroid.
   - Any secondary interior holes (e.g. mug handle, letter counters) shrink to radius zero at their local centroids.
   - The outer contour forms a canonical neutral primitive: a circle ($r = 22\text{ px} – 48\text{ px}$) or a rounded capsule.
2. **Phase 2: Bloom into Target (8 to 12 frames):**
   - The neutral primitive expands outward into the 240 perimeter vertices of Shape $B$.
   - Any target interior holes emerge from the centroid and expand to their final geometry.
3. **Squash, Stretch & Axial Tilt:**
   - At the midpoint transition point ($t = 0.5$), the neutral primitive undergoes 10% to 15% velocity-aligned elongation ($\text{scale}_x, \text{scale}_y$) and a slight axial tilt of $6^{\circ}$ to $14^{\circ}$.

---

## 3. Computational Geometry Pipeline (`lib/morph.js`)

All silhouette transformations follow a deterministic 5-stage geometric pipeline:

### Step 1: Perimeter Arc-Length Resampling (`resamplePoly`)
Every SVG path is sampled into exactly $N = 240$ equidistant perimeter vertices:
$$\text{length}(P) = \sum_{i=1}^M \| p_i - p_{i-1} \|, \quad s_k = \frac{k}{N} \cdot \text{length}(P)$$
This guarantees identical vertex count and uniform point density across all silhouettes.

### Step 2: Winding Order Normalization (`orient`)
Calculate signed area via the Shoelace formula:
$$\text{area}(P) = \frac{1}{2} \sum_{i=0}^{N-1} (x_i y_{i+1} - x_{i+1} y_i)$$
If $\text{area}(P) < 0$, the array is reversed (`P.slice().reverse()`) to ensure clockwise orientation.

### Step 3: Centroid Normalization & Shift Optimization (`bestShift`)
Both polygons are translated to $(0,0)$ via `centroid(P)`. The algorithm computes the circular shift index $s^* \in [0, N-1]$ that minimizes Euclidean point drift:
$$s^* = \operatorname*{arg\,min}_{s} \sum_{i=0}^{N-1} \| A_i - B_{(i+s) \pmod N} \|^2$$
This aligns corresponding corners and eliminates rotational phase spinning.

### Step 4: Neutral Intermediate Primitive Injection (`circ` / `capsule`)
Instead of interpolating directly from $A$ to $B$, the system evaluates:
* For $u \in [0, 0.5]$: `lerpP(A, Neutral, 2 * u)`
* For $u \in [0.5, 1.0]$: `lerpP(Neutral, B, 2 * (u - 0.5))`

### Step 5: Vertex Interpolation with Easing (`lerpP`)
Interpolation evaluates along the canonical morph curve:
$$\text{EM} = \text{cubic-bezier}(0.7, 0, 0.3, 1)$$

---

## 4. Perceptually Uniform Oklab Background Field Wipes

Background color shifts trigger on morph impact frames. To prevent desaturation or muddy midpoints, color blending executes in linear Oklab color space:

```javascript
import { Morph } from '../../lib/morph.js';
const { mixC } = Morph;

// Background field wipe on morph hit
const currentBg = mixC('#16151B', '#FF4F2B', wipeProgress);
```

### Canonical Morph Palette Hierarchy
* **Ink (Dark Ground):** `#16151B`
* **Cream Paper:** `#F4EEE3`
* **Marigold (Warm Accent):** `#FFB627`
* **Vermilion (Hero Energy):** `#FF4F2B`
* **Ultramarine (Deep Accent):** `#2438E8`

---

## 5. Exemplar Metaphor Chains for Diverse Topics

| Topic Domain | Canonical 8-Step Morph Chain |
| :--- | :--- |
| **Travel & Lifestyle (Morphe)** | Drop $\rightarrow$ Coffee Cup $\rightarrow$ Sun $\rightarrow$ Sunset $\rightarrow$ Gull $\rightarrow$ Supersonic Plane $\rightarrow$ Map Pin $\rightarrow$ Heart $\rightarrow$ Wordmark |
| **Healthcare & Medicine** | Pill $\rightarrow$ Stethoscope $\rightarrow$ ECG Pulse Wave $\rightarrow$ Microscope $\rightarrow$ DNA Helix $\rightarrow$ Shield $\rightarrow$ Hospital Cross $\rightarrow$ Identity |
| **Fintech & Growth** | Seed $\rightarrow$ Sprout $\rightarrow$ Coin Stack $\rightarrow$ Credit Card $\rightarrow$ Security Lock $\rightarrow$ Rocket $\rightarrow$ Target Bullseye $\rightarrow$ Brand Mark |
| **Software Architecture** | Terminal Prompt $\rightarrow$ Code Bracket $\rightarrow$ Cloud Node $\rightarrow$ Gear Wheel $\rightarrow$ Database Cylinder $\rightarrow$ Lightning Bolt $\rightarrow$ Checkmark $\rightarrow$ Wordmark |
