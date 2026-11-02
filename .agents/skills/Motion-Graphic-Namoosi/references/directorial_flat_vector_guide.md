# Directorial Guide: Flat Vector 2D (`01-flat-vector`)
## Canonical One-Continuous-Shot Explainer Engine

* **Style Slug:** `01-flat-vector`
* **Benchmark Reference:** Upstream Style 03 (Popwise / Buck / Ordinary Folk / Google Material)
* **Default Rhythm:** 120 BPM (1 beat = 0.50s = 15 frames at 30 FPS)
* **Standard Duration:** 10.00 seconds (300 frames)

---

## 1. Directorial Narrative Doctrine

Flat Vector 2D is **never an animated slide deck**. It is a single, uninterrupted spatial journey where a primary entity transforms, navigates space, triggers environmental escalations, and resolves into a brand wordmark.

```
[Slot 1: HookSubject] ──► [Slot 2: EnvironmentEscalation] ──► [Slot 3: FocalInteraction] ──► [Slot 4: MetricResolution]
```

### Prohibited Anti-Patterns (Automatic Failures)
* **Static Slide Cuts:** Cutting to a blank screen or crossfading between disconnected screens (`DISCONNECTED_SLIDE_DEFECT`).
* **Text Slide Deck UI:** Displaying paragraph explanations, bulleted lists, or floating rectangular UI cards (`SLIDE_DECK_REGRESSION`).
* **Isolated Unmotivated Icons:** Spawning icons in space without geometric connection to the hero entity.

---

## 2. The 4-Act Semantic Slot Storyboard Grammar

Every Flat Vector piece maps user topic briefs into the following 4 semantic acts:

### Act 1: The Kinetic Hook (0.00s to 1.20s / Frames 0–36) — `HookSubject`
* **Directorial Intent:** Establish instant kinetic energy from frame 0. No static pre-roll.
* **Choreography Sequence:**
  1. **Frame 0–14:** The primary entity enters with downward velocity (already in motion at frame 0).
  2. **Frame 15 (`impact1`):** Ground contact with velocity-driven squash deformation ($k = -0.22$, area preserved).
  3. **Frame 16–26:** Elastic rebound with damped oscillation.
  4. **Frame 27–30 (`anticipation`):** Pullback in reverse direction ($4\%$ to $10\%$ reverse displacement over 3–4 frames).
  5. **Frame 31 (`launch`):** Explosive upward release with elongation stretch along the motion vector.
  6. **Frame 40 (`sunLand`):** Entity blooms at apex, bursting $N \ge 8$ radial accent rays.

### Act 2: World Escalation & Camera Push (1.20s to 3.00s / Frames 36–90) — `EnvironmentEscalation`
* **Directorial Intent:** Build contextual visual world through staggered emergence, then push camera focus into the primary scene.
* **Choreography Sequence:**
  1. **Frame 44–80 (`bldStart`):** Contextual structures emerge center-out with a 3-frame stagger (`stagger(i, baseTime, 3)`), using elastic overshoot (`overshootEase`).
  2. **Frame 50–70:** Atmospheric secondary elements (clouds, birds, floating data badges) traverse horizontally across the field.
  3. **Frame 84–90 (`cameraPush`):** Continuous camera zoom and pan ($z$-axis scaling and $(cx, cy)$ tracking) homing in on the focal subject's environment.

### Act 3: Subject Action & Element-Driven Shape Wipe (3.00s to 5.50s / Frames 90–165) — `FocalInteraction`
* **Directorial Intent:** Character or core process action, culminating in an element-driven zero-cut transition.
* **Choreography Sequence:**
  1. **Frame 90–112 (`charArrive`):** Seamless arrival inside interior space. Geometric character/diagram rig with 2-segment limbs (upper and lower rotating segments). Character blinks at frame 114.
  2. **Frame 120–144 (`notificationPop`):** Subject interaction triggers a spring pop badge ($f = 2.6\text{ Hz}, \zeta = 0.38$).
  3. **Frame 144–149 (`bubbleAntic`):** Element contracts slightly in anticipation.
  4. **Frame 150–165 (`shapeWipe`):** The focal element expands exponentially, driving a full-screen circular mask (`clipShapeWipe`) that sweeps the interior scene off screen.

### Act 4: Rhythmic Choreography & Active Lockup (5.50s to 10.00s / Frames 165–300) — `MetricResolution`
* **Directorial Intent:** Rhythmic climax on musical downbeats, morphing into final brand identity with continuous living motion.
* **Choreography Sequence:**
  1. **Frame 165–225:** Hero primitive squirts out of the wipe center, hopping across 4 graphic quadrants precisely on the 4 downbeats ($t = 6.0\text{ s}, 6.5\text{ s}, 7.0\text{ s}, 7.5\text{ s}$).
  2. **Frame 225–239 (`coinFlip`):** Primitive flips edge-on (cosine projection) into a metric token/coin, then zips into a chart bar.
  3. **Frame 240–255 (`logoSettle`):** The bar and primitive morph continuously into the brand wordmark/title.
  4. **Frame 255–300:** Active hold with micro-motion oscillations (periodic subtle scale modulation; no frozen frames).

---

## 3. Color Palette Architecture

Flat Vector uses 5 to 6 pure, saturated, ungradiented tones with strict role separation:

| Role | Tone Name | Hex Code | Visual Application |
| :--- | :--- | :--- | :--- |
| **Field (Base)** | Ultramarine | `#2B2BFF` | Dominant sky / canvas background |
| **Hero / Energy** | Coral | `#FF5A4E` | Primary hero entity, impacts, rays |
| **Accent / Warm** | Sunflower | `#FFC62B` | Sun, coins, key highlights |
| **Secondary Fresh** | Mint | `#2EE6A8` | Ground accent, foliage, metrics |
| **Neutral Surface** | Cream | `#FFF6E9` | Architectural structures, characters, wordmarks |
| **Contrast / Shadow**| Deep Ink | `#151433` | Ground line, character hair, typography |

---

## 4. Kinematics & Physics Implementation

Choreography relies on the closed-form mathematical functions in `lib/motion.js`:

```javascript
import { MotionCraft } from '../../lib/motion.js';
const { spring, pop, anticipation, stagger, applySquashStretch, clipShapeWipe } = MotionCraft;

// 1. Velocity-driven squash & stretch on impact
applySquashStretch(ctx, x, y, vx, vy, 0.0015, () => {
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
});

// 2. Damped spring pop with settle threshold pinning
const [scale, squash] = pop(t, t0, 2.4, 0.42, 0.12, 0.9);

// 3. Circular element-driven shape wipe
clipShapeWipe(ctx, cx, cy, wipeRadius, () => {
  renderScene2(ctx, t);
});
```

---

## 5. Exemplar Mapping Table (Arbitrary Topics)

| Topic Brief | Slot 1: HookSubject | Slot 2: EnvironmentEscalation | Slot 3: FocalInteraction | Slot 4: MetricResolution |
| :--- | :--- | :--- | :--- | :--- |
| **Tech/Finance (Popwise)** | Coral dot $\rightarrow$ Sun | 9 skyscrapers skyline | Office analyst + notification bell | 4-quadrant hop $\rightarrow$ coin flip $\rightarrow$ wordmark |
| **Medical / Cardiology** | Blood cell $\rightarrow$ Heart pulse | Circulatory vessel network | Cardiologist examining ECG monitor | Rhythm pulse $\rightarrow$ stethoscope morph $\rightarrow$ clinic logo |
| **AI / Cloud Infrastructure** | Glowing data packet $\rightarrow$ Core | Server racks & fiber cables | Engineer deploying neural network | Cluster nodes $\rightarrow$ latency graph $\rightarrow$ platform mark |
