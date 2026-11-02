# Consolidated EGM Review Report: Motion Director Dynamic Directing & Asset Integration Engine

* **Target Document:** [`docs/designs/motion_director_dynamic_directing_and_asset_integration.md`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/docs/designs/motion_director_dynamic_directing_and_asset_integration.md)
* **Date:** 2026-11-01
* **Review Mode:** Full Parallel Swarm (7 Zero-Context Goldfish Reviewers)
* **Status:** **REVISION REQUIRED (4 Blockers, 7 Majors, 6 Nits)**

---

## 1. Executive Summary & Verdict

The 7 independent, zero-context Goldfish reviewers evaluated the design document across the full scope (Lines 1–392). 

**Overall Verdict:** The document correctly diagnoses the user's observed failure modes (directorial slide-deck inertia, stiff linear transitions, and naked unstyled image pasting) and establishes the correct 4-beat kinetic standard. However, the technical implementation details contain **critical runtime blockers** (undefined fallback methods, missing geometric methods, and canvas exceptions), **architectural over-engineering** (modifying the agnostic `render.mjs` harness rather than providing modular libraries), and **mathematical imprecision** (Penner polynomial velocity spikes vs true springs).

Implementation cannot proceed until these findings are resolved in the design document.

---

## 2. Consolidated Findings Matrix

| ID | Category | Severity | Description | Source Reviewer(s) |
| :--- | :--- | :--- | :--- | :--- |
| **B-01** | Runtime Crash | 🔴 **Blocker** | `ImagePlates.createFallbackPlaceholder` is called in `preload()` catch block but nowhere defined; fatal `TypeError` on missing/404 image. | `egm-comprehension`, `egm-design`, `egm-implementation-readiness` |
| **B-02** | Missing Implementation | 🔴 **Blocker** | `drawIsometricPlate` is promised across CUJ 2, architecture diagrams, and tables, but omitted from code. | `egm-comprehension`, `egm-design`, `egm-implementation-readiness` |
| **B-03** | Canvas Exception | 🔴 **Blocker** | `drawImageCover` evaluates `naturalWidth / naturalHeight` without zero/NaN/canvas fallback guards; triggers Canvas `IndexSizeError`. | `egm-design` |
| **B-04** | Harness Pollution | 🔴 **Blocker** | Injecting canvas-specific code and custom preload gates into `harness/render.mjs` couples a generic headless runner to 2D canvas; breaks WebGL/SVG/Three.js styles. | `egm-zoom-out` |
| **M-01** | Math Impurity | 🟡 **Major** | `overshoot` uses Penner's `easeOutBack` with initial velocity spike $f'(-1) = 4.56$ rather than true zero-velocity start or damped harmonic spring. | `egm-design`, `egm-zoom-out` |
| **M-02** | Coordinate Transform | 🟡 **Major** | `squashStretch` returns scalars without a rotational transform helper or numerical velocity differentiation $(P(t) - P(t-\Delta t))/\Delta t$. | `egm-design` |
| **M-03** | Transition Semantics | 🟡 **Major** | `drawShapeWipe` is a solid color fill circle rather than a clipping mask (`ctx.clip()`) or layer mask; does not achieve zero-cut element transition. | `egm-design`, `egm-comprehension` |
| **M-04** | Concurrency / VRAM | 🟡 **Major** | Parallel Chrome workers in `render.mjs` decoding high-res images cause GPU memory exhaustion and crashes. | `egm-design` |
| **M-05** | Synchronization Race | 🟡 **Major** | Desynchronization between async `ImagePlates.preload()` and `window.__ready = true` causes frame 0 to capture blank/unloaded plates. | `egm-design`, `egm-comprehension`, `egm-implementation-readiness` |
| **M-06** | Modularity / Packaging | 🟡 **Major** | Scope collision between ESM `export const` and browser global `window.MotionCraft`; missing dual ESM/global export contract. | `egm-comprehension`, `egm-implementation-readiness` |
| **M-07** | Spec Inflation | 🟡 **Major** | Inflating prompt rules into "SemanticMetaphorEngine" software, and over-promising unverified halftone shaders. | `egm-zoom-out`, `egm-style` |
| **N-01** | Code Reuse | 🟢 **Nit** | Re-implementing math from scratch instead of extracting proven `pop()`, `spring()`, `bezier()` from `demos/01-flat-vector/index.html`. | `egm-zoom-out` |
| **N-02** | Aspect Ratio | 🟢 **Nit** | `drawSticker` assumes 1:1 square aspect ratio, distorting 3:4 portrait or 16:9 landscape photographs. | `egm-design`, `egm-zoom-out` |
| **N-03** | Math Edge Case | 🟢 **Nit** | `anticipation` divides by zero if `dur <= 0`. | `egm-design` |
| **N-04** | Missing Sections | 🟢 **Nit** | Feature spec lacks explicit Security/Privacy, Observability/Testing, and Risks/Mitigations sections. | `egm-structural` |
| **N-05** | Formatting / Links | 🟢 **Nit** | Markdown uses inconsistent horizontal rules and unlinked code spans. | `egm-structural` |
| **N-06** | External Deps | 🟢 **Nit** | Demo `19-paperclip` in benchmark repo imports `d3` and `topojson-client`; must clarify whether these are required or stripped. | `egm-codebase-details` |

---

## 3. Actionable Remediation Plan

To resolve all findings and advance to Phase 1 implementation, `docs/designs/motion_director_dynamic_directing_and_asset_integration.md` will be updated with the following definitive solutions:

### Remediation 1: Decouple Harness & Establish Clean Modular Libraries (Resolves B-04, M-06)
* **Leave `harness/render.mjs` untouched:** `render.mjs` remains a clean, agnostic runner that only awaits `window.__ready === true` and evaluates `window.renderAt(t)`.
* **Place modules in `lib/motion.js` and `lib/image_plates.js`:**
  - Written as standard ES modules with universal attachment:
    ```javascript
    export const MotionCraft = { ... };
    if (typeof window !== 'undefined') window.MotionCraft = MotionCraft;
    ```
  - Demos import them cleanly via `<script type="module" src="/lib/motion.js"></script>` or ES import.
  - Image preloading is handled natively inside the demo's init sequence before flipping `window.__ready = true`:
    ```javascript
    const assets = await ImagePlates.preload({ photo: 'assets/hero.jpg' });
    window.__ready = true;
    ```
    This completely eliminates the harness synchronization race (M-05).

### Remediation 2: Add Missing Implementations & Exception Safety (Resolves B-01, B-02, B-03)
* **Define `ImagePlates.createFallbackPlaceholder(key, w = 512, h = 512)`:**
  - Procedurally draws a neutral slate canvas with geometric accent border, initials, and asset key label. Returns the canvas element, which satisfies the `CanvasImageSource` interface.
* **Define `ImagePlates.drawIsometricPlate(ctx, img, x, y, w, h, angle = Math.PI / 6)`:**
  - Applies 30° orthographic affine transform `ctx.transform(Math.cos(angle), Math.sin(angle), -Math.cos(angle), Math.sin(angle), x, y)`, casts a soft underlay shadow, and draws the image.
* **Safe `drawImageCover`:**
  - Safeguard dimension extraction:
    ```javascript
    const nw = img.naturalWidth || img.width || 1;
    const nh = img.naturalHeight || img.height || 1;
    ```
  - Clamps destination width/height $\ge 1$ to prevent `IndexSizeError`.

### Remediation 3: Kinetic Precision & Transformation Helpers (Resolves M-01, M-02, M-03, N-01)
* **Extract proven kinematics from `demos/01-flat-vector/index.html`:**
  - Use true Newton-Raphson `bezier(0.34, 1.56, 0.64, 1)`.
  - Use damped harmonic oscillator `spring(t, f, z)`, `springV(t, f, z)`, and `pop(t, t0, f, z, amt, pin)` where initial velocity is continuous and zero at $t < t_0$.
* **Add `applySquashStretch` helper:**
  - Takes `(ctx, x, y, vx, vy, k, drawFn)`, rotates canvas by `Math.atan2(vy, vx)`, applies `ctx.scale(stretch, squash)`, and draws the element.
* **Refactor `clipShapeWipe`:**
  - Masks the canvas: `ctx.beginPath(); ctx.arc(cx, cy, radius, 0, Math.PI * 2); ctx.clip();`.

### Remediation 4: Directorial Governance & Technical De-fluffing (Resolves M-07, N-04, N-05, N-06)
* Re-scope "SemanticMetaphorEngine" as directorial prompt governance in `SKILL.md` (no fake software claims).
* Strip inflated marketing terms; frame constraints neutrally ("Typography Constraint: Max 1–3 words per act").
* Add standard sections: Security/Asset Isolation, Observability/Integrity Tests, Risks & Mitigations.
* Strip `d3` / `topojson-client` from `19-paperclip` port: replace complex geopolitical maps with lightweight vector path diagrams and photographic plates to maintain zero-dependency purity.
