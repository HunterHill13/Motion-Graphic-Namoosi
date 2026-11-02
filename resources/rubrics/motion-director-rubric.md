# Motion Director Quality Rubric (7-Dimension Studio Standards)

Adapted from international motion design benchmarks (Buck, ManvsMachine, Ordinary Folk, Giant Ant, Apple Keynote, Pentagram). Used by the independent zero-context auditor (`motion-director-auditor`) to evaluate all films before delivery.

Target Score: $\ge 8.0 / 10.0$ in every dimension. Any score $< 7.0$ triggers immediate rejection (`REJECTED`) and auto-revision.

---

## 1. The 7 Scoring Dimensions

### 1. `style_fidelity` (Canonical Style Authenticity)
* **Score 1–4:** Unrecognizable style, generic AI template feel, mixed contradictory styles.
* **Score 5–6:** Basic attributes present but lacks canonical techniques (e.g., flat vector without squash/stretch; morphing with ugly vertex knots).
* **Score 7–8:** Instantly recognizable in 1 second. All signature techniques present and correctly executed (e.g. 3-phase anticipation, shape wipes, 240-vertex morph bridge).
* **Score 9–10:** Award-shortlist quality. Flawless execution matching top design studio reels.

### 2. `concept_wow` (Idea, Hook & Arc)
* **Score 1–4:** Boring presentation slides, static text paragraphs, slow or empty opening (> 0.5s dead black/void).
* **Score 5–6:** Competent topic explainer, but predictable transitions and no memorable hero moment.
* **Score 7–8:** Strong concept. Hook hits within first 0.5s. Clear escalation. Unmistakable hero climax at 60–75% of runtime. Composed living end frame held for 0.8–1.2s.
* **Score 9–10:** Jaw-dropping visual metaphor, clever concept execution, unforgettable pacing.

### 3. `motion_craft` (Physics, Easing & Choreography)
* **Score 1–4:** Linear easing, rigid CSS transitions, jittery frame drops, random camera pans disguising dead elements. Direct shape-to-shape morphing without neutral collapse. Static cuts between disconnected screens.
* **Score 5–6:** Basic easing applied, but lacks anticipation, follow-through, or velocity-driven deformation.
* **Score 7–8:** Purposeful physical easing (`cubic-bezier(0.34, 1.56, 0.64, 1)` or damped harmonic springs from `lib/motion.js`). Velocity-driven squash & stretch ($\approx 10\%-15\%$). 2–4 frame stagger. Only one hero element moves at a time.
  - **For Style 01 (`01-flat-vector`):** Element-driven transitions (exponential circular shape wipes `clipShapeWipe` or continuous camera pushes).
  - **For Style 08 (`08-morph`):** Strict two-phase collapse requirement: complex shapes collapse into an intermediate neutral primitive (circle or capsule) over 8–12 frames before blooming into the target silhouette.
* **Score 9–10:** Masterful secondary action, fluid arcs, sub-frame motion blur, perfect weight and momentum.

### 4. `design_typography` (Composition, Hierarchy & Text Setting)
* **Score 1–4:** Text paragraphs or bullet points on screen, broken Persian ligatures, cluttered corners, no grid.
* **Score 5–6:** Decent layout, but too much text or weak typographic weight contrast.
* **Score 7–8:** Strict typographic restraint (monumental 1–3 word kinetic verbal punches, no paragraphs). Perfect Persian cursive ligatures. Controlled 5–6 color palette. Generous negative space and Swiss/Material grid.
* **Score 9–10:** World-class graphic design layout, bespoke glyph integration, flawless typographic poise.

### 5. `finish_texture` (Atmosphere, Materiality & Shaders)
* **Score 1–4:** Flat unshaded vector, heavy banding in gradients, harsh digital clipping.
* **Score 5–6:** Standard clean render, but feels sterile or plastic.
* **Score 7–8:** Intentional texture and depth appropriate to the style (e.g., 3–5% dither noise preventing banding, Oklab color grading, subtle caustics/glow, soft ambient shadows in isometric).
* **Score 9–10:** Film-grade finish, physical lighting, organic material feel.

### 6. `sound_sync` (Musicality, Sound Design & Hit Locking)
* **Score 1–4:** Mismatched generic BGM, sound out of sync with visual impacts, unmastered volume.
* **Score 5–6:** BGM plays alongside animation, but hits are loosely aligned.
* **Score 7–8:** Master frame cue sheet (`cues.json`) tightly binds picture and sound. Every pop, whoosh, bounce, and impact lands on the exact visual frame. Mastered to EBU R128 (-14 LUFS integrated, true peak $\le -1.1$ dBTP).
* **Score 9–10:** Sublime musicality, punchy tactile transients, perfect frequency balance.

### 7. `technical` (Spec Compliance & Determinism)
* **Score 1–4:** Incorrect frame rate/duration, console errors, missing assets, dropped frames.
* **Score 5–6:** Render finishes, but minor font fallbacks or subpixel shimmering visible.
* **Score 7–8:** Exact duration (e.g. exactly 10.000s / 300 frames @ 30fps), 1080p, H.264 stereo AAC, 100% deterministic (pure function of time $t$), zero console warnings.
* **Score 9–10:** Completely bulletproof render pipeline, zero defects.

---

## 2. Fatal Defect Flags (Immediate Automatic REJECT)

If ANY of the following defect codes are detected, the film is automatically marked **`REJECTED`** with a mandatory revision cycle:

1. **`SLIDE_DECK_REGRESSION`:**
   * Any paragraph of explanatory body text, bullet points, informational cards, or more than 3 words per act rendered simultaneously.
2. **`NAKED_IMAGE_DEFECT`:**
   * Any photograph or raster image pasted into the scene as an unmasked, unstyled rectangular bitmap. Images must use `lib/image_plates.js` (Sticker squircle with white border, Collage with scissor border and 12fps jitter, or 2.5D Isometric Plate).
3. **`STIFF_MOTION_DEFECT`:**
   * Linear easing ($x = t \cdot v$), un-cushioned mechanical arrivals, or movement lacking 3-phase anticipation pullback (-4% to -10%) and overshoot settle.
4. **`PRELOAD_TIMEOUT_RISK`:**
   * Images loaded without asynchronous preloading (`await ImagePlates.preload(manifest)`) or lacking fallback monogram safety, exposing the render to 404 hangs.
5. **`MISSING_CUE_ALIGNMENT`:**
   * Visual impact frames diverging from the corresponding audio SFX events in `cues.json`.
6. **`BROKEN_PERSIAN_LIGATURES`:**
   * Persian or Arabic letters rendered detached, backwards, or reversed due to lack of BiDi handling.
7. **`STATIC_HOLD_OPENING`:**
   * Scene lingering on empty canvas or static void for $> 0.3$s at the start. Frame 0 must burst with kinetic energy.
8. **`DIRECT_SHAPE_MORPH_DEFECT`:**
   * In Style 08 (`08-morph`), attempting direct shape-to-shape morphing between complex silhouettes without collapsing through an intermediate neutral primitive (circle or capsule) over 8–12 frames.
9. **`DISCONNECTED_SLIDE_DEFECT`:**
   * In Style 01 (`01-flat-vector`), executing cuts to black or crossfades between isolated static scenes instead of continuous spatial camera push or element-driven shape wipes (`clipShapeWipe`).
10. **`VOICEOVER_DESYNC_DEFECT`:**
   * Any voiceover audio track injected as an unaligned monolithic file at $t = 0.0$ without per-shot segmentation or word-boundary timestamp extraction.
   * Any shot or transition where the spoken narration refers to an element not yet on screen or long gone ($> 100$ms discrepancy).
   * Any hardcoded time floats in `index.html` bypassing `cues.frames[...]` or scene transitions occurring off musical beat boundaries (`snapToBeat`).
