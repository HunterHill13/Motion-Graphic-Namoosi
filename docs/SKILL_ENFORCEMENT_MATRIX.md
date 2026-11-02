# Skill Enforcement Matrix

## 1. Enforcement Level Definitions
To prevent "documentation-only" claims and eliminate false passes, every requirement in the skill is classified into an explicit enforcement tier:
- **`RULE ONLY`**: Stated in markdown as a guideline. Easily ignored or misunderstood by the agent. Zero mechanical check.
- **`PLANNING RULE`**: Validated during pre-production (e.g. in `SHOTBOOK.md` or `VisualStateGraph`). Blocks code authoring if invalid.
- **`CODE ENFORCED`**: Verified by TypeScript types, lint scripts, or static analysis before compilation.
- **`RENDER ENFORCED`**: Verified by computer vision, frame diffing, acoustic analysis, or blind review on the rendered output files.

---

## 2. Enforcement Audit Table

| Rule / Mandate | Current Level | Desired Level | Enforcement Gap | Concrete Repair |
| :--- | :--- | :--- | :--- | :--- |
| **No Slideshows / Anti-Slideshow** | `RULE ONLY` | `RENDER ENFORCED` | Prose prohibited slideshows, but agent created card-per-sentence layouts and called it animation. | Introduce `ANTI_SLIDESHOW_GATE` inspecting frame diffs and state transformations; detect signatures S1–S8. |
| **Meaningful Visual Transformation** | `RULE ONLY` | `PLANNING RULE` + `RENDER ENFORCED` | Agent treated text fade-in and translateY springs as "visual transformation." | Require explicit `VisualStateGraph` in Shotbook. Opacity changes do NOT count as motion events. |
| **Voice Speed & Natural Prosody** | `RULE ONLY` (Poisoned) | `RENDER ENFORCED` | Agent passed "بدون شتاب" (slow) to TTS, producing sluggish audio under 95 WPM. | Create `VOICE_SPEED_GATE` measuring audio duration, transcript word count, and WPM (Mandate: 130–165 WPM). |
| **No Orphan Elements** | `PLANNING RULE` | `PLANNING RULE` + `CODE ENFORCED` | Declared in causal graph markdown, but orphan UI remained in rendered JSX. | Add `REMOVAL_TEST_GATE`: If an element's removal does not harm narrative meaning, it MUST be deleted. |
| **Element Budget ($\le 7$ Active)** | `RULE ONLY` | `PLANNING RULE` + `CODE ENFORCED` | Agent added decorative telemetry, ticks, and borders that exceeded visual capacity. | Require strict component role declarations (`HERO`, `SUPPORT`, `ENVIRONMENT`). Disallow undeclared decorative elements. |
| **Camera Purpose vs. Fake Animation** | `RULE ONLY` (Poisoned) | `RENDER ENFORCED` | Agent used 1.00 $\to$ 1.05 continuous camera zoom to fake activity on static slides. | Mandate that camera zoom alone NEVER counts as a motion event. Subordinate camera to subject consequence. |
| **Zero-Subpixel Jitter** | `CODE ENFORCED` | `RENDER ENFORCED` | Sanitizer stripped diacritics, but text sometimes vibrated during continuous transforms. | Enforce integer rounding (`Math.round`), `translate3d(0,0,0)`, and CSS `backface-visibility: hidden`. |
| **Dual-Script Architecture** | `CODE ENFORCED` | `CODE ENFORCED` | Already cleanly implemented in `persianSanitizer.ts`. | Enforce that visual strings MUST pass through `sanitizeForDisplay()`. |
| **Independent Blind Review** | `RULE ONLY` | `RENDER ENFORCED` | Agent self-reviewed its own code and rubber-stamped a 9/10 score. | Mandate Blind Review protocol: reviewer inspects only rendered MP4/WAV without seeing code claims or self-praise. |
| **Intentional Stillness** | `RULE ONLY` | `RENDER ENFORCED` | Agent used "stillness is power" as an excuse for 5-second dead holds. | Differentiate `JUSTIFIED STILLNESS` (1.0–2.5s post-impact reading hold) from `UNJUSTIFIED HOLD` (dead screen). |
| **Motion-Carry Transitions** | `RULE ONLY` | `PLANNING RULE` + `RENDER ENFORCED` | Agent defaulted to `<ShotTransition type="fade" />`. | Purge generic fade from template; require physical trajectory handoff between beats. |
| **Exclusive Gemini TTS (`Puck`)** | `CODE ENFORCED` | `CODE ENFORCED` | Replaced Edge-TTS with Gemini API in scripts; fail-closed is active. | Maintain fail-closed architecture; block any build without Gemini API. |

---

## 3. Immediate Action Items
1. **Promote `VOICE_SPEED_GATE` to RENDER ENFORCED:** Build `tests/skill-regression/check_voice_speed.py`.
2. **Promote `ANTI_SLIDESHOW_GATE` to RENDER ENFORCED:** Build `tests/skill-regression/check_slideshow_signatures.py`.
3. **Purge Poisoned Guidelines from References:**
   - Remove "بدون شتاب" from TTS references $\to$ replace with `references/voice-doctrine.md`.
   - Remove "continuous camera zoom as scene life" from `references/living-motion.md` $\to$ replace with `references/motion-doctrine.md`.
   - Purge `fade` from `template/src/motion/transitions.tsx`.
