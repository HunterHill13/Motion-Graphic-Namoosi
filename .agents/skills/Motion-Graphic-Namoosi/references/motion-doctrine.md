# Single Authoritative Motion Doctrine

## 1. The Core Creed
```text
Motion exists because something changes.
Something changes because the story requires it.
The camera participates because the visual consequence requires it.
Stillness exists because the viewer needs to read or feel the result.
Transitions exist because state A leads to state B.
Nothing moves merely to prevent a static frame.
```

---

## 2. The Absolute Hierarchy of Visual Design
Every motion decision must be authorized by this strict descending hierarchy:
```text
1. NARRATIVE PURPOSE          (What idea is being communicated?)
2. SEMANTIC TRANSFORMATION    (How does the visual entity physically become that idea?)
3. PHYSICAL/SPATIAL CAUSALITY (What force or ancestor object caused this action?)
4. MOTION CHOREOGRAPHY        (Authored acceleration, velocity handoff, inertia, settle)
5. CAMERA PARTICIPATION       (Does the camera follow consequence, reveal scale, or reframe?)
6. DECORATIVE MOTION          (STRICTLY LAST: Micro-accents, rim flashes, subtle textures)
```

### The Iron Rule of Decorative Motion:
> **Decorative motion must NEVER compensate for the absence of meaningful visual transformation.**  
> A slow camera zoom on a static card is NOT cinematic motion.  
> Text fading in on a dark void is NOT a visual event.

---

## 3. Definition of a "Meaningful Visual Transformation"
A visual event is only recognized as a meaningful transformation if it physically alters at least one of the following:
1. **Object Identity:** Shape $A$ physically unlatching, morphing, or unfolding into Object $B$.
2. **Object State:** A mechanical component moving from closed $\to$ articulated $\to$ elevated.
3. **Spatial Relationship:** Entities grouping, docking, separating, or forming an architectural alignment.
4. **Material State:** Surface changing from matte $\to$ illuminated $\to$ translucent $\to$ stressed.
5. **Geometry:** Extrusion from 2D plane into 3D perspective depth, or structural bifurcation.
6. **Information Hierarchy:** A secondary node promoting to primary hero via physical momentum.
7. **Causal Consequence:** Deceleration of Entity $A$ triggering an electrical/mechanical surge that launches Entity $B$.

### What is FORBIDDEN as a "Visual Event":
- Fading opacity from 0 to 1 on an isolated text block.
- Sliding an element up by 20 pixels without interaction or impact.
- Bouncing text words into a static card (`WordReveal`).
- Continuous sinusoidal camera breathing on an otherwise dead frame.
- Ambient dust particles floating in the background.

---

## 4. The VisualStateGraph Planning Abstraction
Before any Remotion code is written, every major narrative beat must be mapped as a node in the **VisualStateGraph**:

```typescript
export interface VisualStateNode {
  stateId: string;             // e.g. "S01_CALIBRATION"
  semanticPurpose: string;     // Narrative goal (e.g. "Establish statutory baseline")
  heroElement: string;         // The single primary visual actor (e.g. "Kinetic Monolith")
  supportingElements: string[];// Max 1-2 supporting entities (e.g. ["Foundation Rail"])
  currentState: string;        // Visual form before the beat (e.g. "Closed titanium cylinder")
  trigger: string;             // Auditory/narrative trigger (e.g. "Spoken keyword 'بند کاف'")
  transformation: string;      // Physical mechanism (e.g. "Splits vertically along central seam")
  destinationState: string;    // Resulting form (e.g. "Bifurcated dual pillar with exposed core")
  consequence: string;         // Downstream reaction (e.g. "Kinetic pulse travels down rail")
  cameraPurpose: string;       // Motivated camera action (e.g. "Pans right following kinetic pulse")
  audioEvent: string;          // Synchronized acoustic transient (e.g. "Hydraulic pressure hiss + sub-drop")
  elementsToDelete: string[];  // Entities whose utility ended and must exit
}
```

If the director cannot articulate the `transformation` and `consequence`, the beat is **UNPREPARED FOR PRODUCTION**.

---

## 5. Meaningful Motion Event Density
Do NOT measure visual vitality by clock intervals (e.g. "something moves every 3 seconds").  
Measure **Meaningful Motion Event Density**:
$$\text{Density} = \frac{\text{Transformations} + \text{Causal Handoffs} + \text{Spatial Disclosures}}{\text{Total Narrative Beats}}$$
- A 20-second sequence with 10 text fades has a Meaningful Density of **0**.
- A 20-second sequence with 3 mechanical unlatchings, 2 momentum handoffs, and 1 camera crane reveal has a Meaningful Density of **6** (Gold Standard).

---

## 6. Intentional Stillness vs. Dead Holds
- **`JUSTIFIED STILLNESS` (1.0s – 2.5s):** Follows a high-velocity physical impact or structural lock. Allows the viewer's eye to digest the stabilized information. Coordinates are locked (`Math.round`), transforms are clamped, and the frame rests with certainty.
- **`UNJUSTIFIED HOLD` (BANNED):** Screen remains static merely because the agent did not author an animation. If a scene remains static for $> 2.5\text{s}$ without an arrival impact or reading justification, it fails the `STATIC_HOLD_AUDIT`.
