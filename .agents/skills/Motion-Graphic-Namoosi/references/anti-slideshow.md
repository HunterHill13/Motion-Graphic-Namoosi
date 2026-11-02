# Anti-Slideshow Signatures & Detection Specification

## Overview
The `ANTI_SLIDESHOW_GATE` evaluates compositions against eight detectable signatures of automated slideshow behavior. A production exhibiting two or more of these signatures is **immediately disqualified**.

---

### Signature S1: Unmotivated Scene Replacement
* **SIGNATURE:** Scene $N+1$ wipes or dissolves over Scene $N$ without a causal momentum or spatial handoff.
* **WHY IT FAILS:** Breaks the viewer's mental model of physical reality. Reverts the video to PowerPoint slide swaps.
* **DETECTION METHOD:** Frame differencing shows complete screen-wide pixel turnover across 1–15 frames while camera position resets to $(0,0,0)$.
* **ACCEPTABLE ALTERNATIVE:** Use **Motion-Carry** (object from Scene $N$ exits at velocity $V$ into Scene $N+1$) or **Persistent World Canvas** (camera reframes within the same 3D architecture).

---

### Signature S2: Template Reuse with Text Swapping
* **SIGNATURE:** The background and layout remain identical while only the text paragraph changes.
* **WHY IT FAILS:** Demonstrates zero visual storytelling. The graphic serves as a static placard rather than an embodiment of the idea.
* **DETECTION METHOD:** Structural similarity (SSIM) between consecutive scenes is $> 0.90$, with pixel variance isolated exclusively to text bounding boxes.
* **ACCEPTABLE ALTERNATIVE:** New information must cause a structural metamorphosis (e.g. a cylinder unlatching into three struts, or a plinth telescoping upwards).

---

### Signature S3: Text Block Fade as Primary Motion
* **SIGNATURE:** The primary visual event of a beat is a paragraph or headline fading in (`opacity: 0 -> 1`) or sliding upwards by 20 pixels.
* **WHY IT FAILS:** Reading text is not motion design. It treats video as a book that turns its own pages.
* **DETECTION METHOD:** Over any 3-second window, the only animated CSS properties in the DOM are `opacity` and small `translateY` on text nodes.
* **ACCEPTABLE ALTERNATIVE:** Information is revealed as a mechanical consequence (e.g. sliding titanium shutter, laser engraving, physical flip-wheel indicator).

---

### Signature S4: Camera Zoom as Substitute for Animation
* **SIGNATURE:** A slow push-in or pull-back ($1.00 \to 1.05$) runs continuously while the subject on screen is completely motionless.
* **WHY IT FAILS:** Deceives the viewer with camera drift to mask the lack of actual content choreography.
* **DETECTION METHOD:** Viewport scale varies over time while relative distances between on-screen entities remain $0$.
* **ACCEPTABLE ALTERNATIVE:** Camera moves only to follow an accelerating object, absorb a landing shock, or reframe an expanding physical assembly.

---

### Signature S5: Sequential Card Stacking (The SaaS Tile Trap)
* **SIGNATURE:** 2 to 4 rectangular cards with rounded corners appear sequentially with icons and titles to represent list items.
* **WHY IT FAILS:** Evokes cheap web dashboard templates and PowerPoint templates.
* **DETECTION METHOD:** Multiple rectangular containers with borders and padding appearing in a grid or row.
* **ACCEPTABLE ALTERNATIVE:** Represent criteria as physical entities (e.g. three kinetic plinths rising from bedrock, or three interwoven structural cables carrying tension).

---

### Signature S6: Disappearing Without Transformation (The Vacuum Trap)
* **SIGNATURE:** When an entity is done, it fades to opacity 0 or vanishes into thin air without an exit trajectory or physical deconstruction.
* **WHY IT FAILS:** Violates Mass Conservation and creates orphan visual gaps.
* **DETECTION METHOD:** Object disappears while surrounding elements remain static, with zero kinetic reaction in neighboring nodes.
* **ACCEPTABLE ALTERNATIVE:** The entity folds into the floor rail, morphs into the baseline of the next element, or launches off-screen carrying momentum.

---

### Signature S7: Lack of Persistent Spatial Identity
* **SIGNATURE:** Every 4 seconds, the scene hops to an unrelated coordinate space with different lighting, different background, and zero connection to prior geometry.
* **WHY IT FAILS:** Forces the viewer to re-orient themselves every sentence, destroying cognitive immersion.
* **DETECTION METHOD:** Absence of a shared coordinate space, persistent lighting model, or unifying architectural substrate.
* **ACCEPTABLE ALTERNATIVE:** The Sovereign Calibration Pavilion / Single World Canvas: All events occur within one continuous 3D architectural landscape.

---

### Signature S8: Scene Reset on Sentence Boundary
* **SIGNATURE:** The visual state resets to zero every time the voiceover finishes a grammatical sentence.
* **WHY IT FAILS:** Mechanically couples visual design to grammar rather than narrative ideas.
* **DETECTION METHOD:** 1:1 correlation between voiceover silence segments and Remotion `<Sequence>` start boundaries.
* **ACCEPTABLE ALTERNATIVE:** Visual transformations anticipate sentences, bridge across sentences, or hold past sentence boundaries.
