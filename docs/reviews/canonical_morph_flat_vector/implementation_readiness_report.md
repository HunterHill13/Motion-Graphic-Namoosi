# Implementation Readiness Audit Report: Detailed Implementation Plan (Lines 275–463)

* **Target File:** [`docs/designs/canonical_flat_vector_and_shape_morph_engine.md`](file:///g:/%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87/%DA%A9%D9%85%DB%8C%D8%AA%D9%87%20%D8%AA%D8%AD%D9%82%DB%8C%D9%82%D8%A7%D8%AA%DB%8C/%D9%81%DB%8C%D9%84%D9%85%20%D9%87%D8%A7%20%D9%87%D9%81%D8%AA%DA%AF%DB%8C/%D8%A7%D8%B3%DA%A9%DB%8C%D9%84%20%D9%85%D9%88%D8%B4%D9%86%20%DA%AF%D8%B1%D8%A7%D9%81%DB%8C%DA%A9/docs/designs/canonical_flat_vector_and_shape_morph_engine.md#L275-L463)
* **Audited Scope:** Lines 275–463 (`## Detailed Implementation Plan` through `### Risk Assessment & Mitigation`)
* **Auditing Reviewers:** `egm-implementation-readiness` (Pragmatic Tech Lead), `egm-codebase-details` (Codebase Details Auditor), `egm-style` (Technical Copy Editor)
* **Standards:** [`implementation-readiness-standard.md`](file:///C:/Users/Hill/.gemini/config/plugins/egm/resources/document_standards/implementation-readiness-standard.md) & Plain-English Technical Writing Standard
* **Stage Verdict:** **FAILED / REVISE (5 Blockers, 8 Majors, 10 Nits)**

---

## Executive Summary

The Detailed Implementation Plan provides a coherent five-phase rollout. However, under the strict **Zero-Decision Rule**, the plan cannot be executed cleanly by an independent engineer or AI session without guessing or making unguided design decisions:
1. **Style ID Collision with Codebase Catalog:** Flat Vector is called "Style 03" and Shape Morph is called "Style 06" (in reality, Flat Vector is Style 01, Shape Morph is Style 08, Style 03 is Isometric, and Style 06 is Collage).
2. **Rubric Dimension Collision:** The plan cites non-existent rubric dimensions ("Criterion 2: Transition Fluidity", "Criterion 5: Sound Sync") instead of canonical keys (`concept_wow`, `motion_craft`, `sound_sync`).
3. **`sampleD` Node Execution Gap:** `sampleD` relies on SVG DOM methods (`getTotalLength`, `getPointAtLength`) which do not exist in Node.js, yet pure Node fallback equations are omitted.
4. **Underspecified `capsule()` Primitive:** The geometric piecewise formula, parameter semantics, and vertex arc-length distribution for capsules are left undefined.
5. **Heterogeneous `cues.json` Stills Resolution:** The `--stills` flag extraction heuristics do not define how to resolve diverging cue schemas between `01-flat-vector` (integer `frames`) and `08-morph` (float `land`).
6. **KaTeX & Style Syntax Errors:** Unicode en-dashes inside math mode (`$r = 22\text{px} – 48\text{px}$`), unescaped HTML tags in table cells, and dramatic promotional phrasing.

---

## Detailed Consolidated Findings

### 1. Codebase Alignment & Architectural Decisions

#### Finding IR1 [Blocker]: Style ID Mismatch Contradicts Codebase Catalog & `SKILL.md`
* **Location:** Lines 328, 431, 432
* **Discrepancy:** The plan references Style 03 for Flat Vector and Style 06 for Shape Morph. In [`SKILL.md`](file:///g:/%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87/%DA%A9%D9%85%DB%8C%D8%AA%D9%87%20%D8%AA%D8%AD%D9%82%DB%8C%D9%82%D8%A7%D8%AA%DB%8C/%D9%81%DB%8C%D9%84%D9%85%20%D9%87%D8%A7%20%D9%87%D9%81%D8%AA%DA%AF%DB%8C/%D8%A7%D8%B3%DA%A9%DB%8C%D9%84%20%D9%85%D9%88%D8%B4%D9%86%20%DA%AF%D8%B1%D8%A7%D9%81%DB%8C%DA%A9/.agents/skills/cinematic-motion-director/SKILL.md#L132-L139), Style 01 is `01-flat-vector`, Style 08 is `08-morph`, Style 03 is `03-isometric`, and Style 06 is `06-collage`.
* **Actionable Fix:** Standardize strictly on canonical workspace slugs: **Style 01 (`01-flat-vector`)** and **Style 08 (`08-morph`)**.

#### Finding IR2 [Blocker]: Rubric Criteria Numbering and Dimension Names Contradict Codebase
* **Location:** Lines 425–439 (Phase 4.1)
* **Discrepancy:** Cites "Criterion 2 (Transition Fluidity & Continuity)" and "Criterion 5 (Audio-Visual Synchronization)". The actual rubric in [`resources/rubrics/motion-director-rubric.md`](file:///g:/%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87/%DA%A9%D9%85%DB%8C%D8%AA%D9%87%20%D8%AA%D8%AD%D9%82%DB%8C%D9%82%D8%A7%D8%AA%DB%8C/%D9%81%DB%8C%D9%84%D9%85%20%D9%87%D8%A7%20%D9%87%D9%81%D8%AA%DA%AF%DB%8C/%D8%A7%D8%B3%DA%A9%DB%8C%D9%84%20%D9%85%D9%88%D8%B4%D9%86%20%DA%AF%D8%B1%D8%A7%D9%81%DB%8C%DA%A9/resources/rubrics/motion-director-rubric.md) strictly uses the 7 canonical dimensions: `style_fidelity`, `concept_wow`, `motion_craft`, `design_typography`, `finish_texture`, `sound_sync`, `technical`.
* **Actionable Fix:**
  1. Relocate transition/kinematics rules under Dimension 3 (`motion_craft`).
  2. Relocate audio-visual sync rules under Dimension 6 (`sound_sync`).
  3. Formalize Section 2 Fatal Defect codes: `DIRECT_SHAPE_MORPH_DEFECT` and `DISCONNECTED_SLIDE_DEFECT`.

#### Finding IR3 [Blocker]: Missing Node.js SVG Path Parser / DOM Boundary in `lib/morph.js`
* **Location:** Lines 341–349, 460
* **Discrepancy:** `sampleD` uses SVG DOM methods (`getTotalLength`, `getPointAtLength`) which throw `ReferenceError: document is not defined` in pure Node.js.
* **Actionable Fix:** Explicitly scope `sampleD` as requiring a DOM context (Browser or Puppeteer hidden `<svg>`). In pure Node environments, throw an informative error and test mathematical utilities (`resamplePoly`, `bestShift`, `mixC`) with pre-sampled polygon arrays.

#### Finding IR4 [Blocker]: Undefined Parametric Formulation for `capsule()` Primitive
* **Location:** Lines 384–387
* **Discrepancy:** `capsule(cx, cy, w, h, r, n = 240)` is declared without orientation, bounding box semantics, or arc-length sampling equations.
* **Actionable Fix:** Define $w$ as total width, $h$ as total height, and cap radius $r = \min(w, h)/2$. For horizontal capsule ($w \ge h$), specify the two semicircles centered at $(cx \pm (w/2 - r), cy)$ connected by two linear segments of length $L = w - 2r$, sampled uniformly along perimeter $P = 2L + 2\pi r$.

#### Finding IR5 [Major]: `--stills` CLI & Cue Extraction Heuristics Divergence
* **Location:** Lines 409–420
* **Discrepancy:** Existing `harness/render.mjs` already implements `--stills` via `seek(page, t)`. Furthermore, `01-flat-vector` uses integer `frames` while `08-morph` uses float `land` timestamps.
* **Actionable Fix:** Specify the exact fallback resolution chain:
  ```javascript
  let ts = [];
  if (typeof args.stills === 'string') ts = args.stills.split(',').map(Number);
  else if (cues?.stills) ts = cues.stills.map(Number);
  else if (cues?.frames) ts = ['impact1', 'push', 'wipe', 'burst1', 'logoSettle'].filter(k => cues.frames[k] !== undefined).map(k => cues.frames[k] / (cues.fps || 30));
  else if (cues?.land) ts = Object.values(cues.land).slice(0, 6);
  if (!ts.length) ts = [0.50, 1.35, 3.80, 5.00, 6.50, 9.20];
  ```

#### Finding IR6 [Major]: Missing `manifest.json` Schema & Browser-Side Luminance Check
* **Location:** Lines 418–420
* **Discrepancy:** Node cannot decode PNGs without external dependencies (`sharp`/`pngjs`). `manifest.json` schema is omitted.
* **Actionable Fix:** Perform Rec. 709 luminance check ($Y = 0.2126R + 0.7152G + 0.0722B$) inside Puppeteer via `page.evaluate()` on an offscreen canvas before screenshotting, and provide the exact JSON schema for `manifest.json`.

#### Finding IR7 [Major]: Incomplete Geometry API: Missing `orient`, `area`, `centroid`
* **Location:** Lines 335–403
* **Discrepancy:** `demos/08-morph/index.html` relies on `orient(P)` (Shoelace area formula) and `centroid(P)`. Omitting them causes polygons with opposite winding directions to invert and knot during morphing.
* **Actionable Fix:** Export `orient(P)`, `area(P)`, and `centroid(P)` in `lib/morph.js` along with namespace export `Morph`.

#### Finding IR8 [Major]: Non-Concrete Test Assertions in Phase 5
* **Location:** Lines 443–453
* **Discrepancy:** Test cases use high-level prose without coordinates, tolerance thresholds, or color values.
* **Actionable Fix:** Provide concrete inputs and numeric thresholds for all 5 test cases (unit square perimeter distance $|d_i - 400/240| < 10^{-3}$, circle circular shift alignment, Oklab chroma $\sqrt{a^2+b^2} > 0.04$, `pop(1.0, ...)` strict `[1, 0]`).

---

### 2. Copy Editing & KaTeX Syntax Findings (`egm-style`)

#### Finding ST1 [Blocker]: Unicode En-Dashes in Math Delimiters
* **Location:** Lines 319, 320, 434
* **Exact:** `($r = 22\text{px} – 48\text{px}$)`, `($10\% – 15\%$)`, `($4\% – 10\%$)`
* **Revision:** Use plain text or standard math relations: `($22\text{ px} \le r \le 48\text{ px}$)`, `(10%–15%)`, `(4%–10%)`.

#### Finding ST2 [Blocker]: Unescaped HTML Tags in Markdown Table
* **Location:** Lines 460, 461
* **Exact:** `<svg>`, `< 0`
* **Revision:** Wrap in code backticks: `` `<svg>` ``, `` `< 0` ``.

#### Finding ST3 [Major]: Theatrical Phrasing & Slang
* **Location:** Lines 308, 319, 463
* **Exact:** *"living breathing hold"*, *"The Two-Phase Intermediate Collapse Law"*, *"Blast Radius"*
* **Revision:** Replace with objective technical terms: *"hold with micro-motion oscillation"*, *"Two-Phase Intermediate Collapse Requirement"*, *"Regression Risk on Existing Demos"*.

#### Finding ST4 [Major]: Incomplete JSDoc Docstrings
* **Location:** Lines 374–403
* **Revision:** Add complete `@param` and `@returns` docstrings for `lerpP`, `circ`, `capsule`, `oklab`, `fromOklab`, and `mixC`.

---

## Action Plan for Stage 9 Remediation
1. Correct style slugs to `01-flat-vector` and `08-morph`.
2. Re-align rubric updates with Dimension 3 (`motion_craft`), Dimension 6 (`sound_sync`), and add Fatal Defect codes.
3. Clarify `sampleD` DOM execution boundary, define `capsule()` formula, and export `orient`, `area`, `centroid`.
4. Define `cues.json` stills resolution chain and `manifest.json` schema with in-page luminance evaluation.
5. Provide concrete test inputs and tolerances for `tests/test_directing_engines.mjs`.
6. Fix all KaTeX en-dash syntax errors, unescaped HTML tags in tables, and complete JSDoc docstrings.
