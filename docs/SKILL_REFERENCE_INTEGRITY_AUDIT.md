# Skill Reference & Integrity Audit

## Executive Summary
This audit inspects every internal reference, imported markdown file, script path, and template component in `.agents/skills/cinematic-motion-director/` to identify dead references, conflicting rules, and architectural disconnects.

---

## 1. Reference Integrity Table

| Referenced File / Symbol | Location / Origin | Exists | Actually Read | Still Authoritative | Conflicts with Another Rule | Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `references/causal-planning.md` | Skill `references/` | **YES** | **YES** | **PARTIAL** | Emphasizes causal graphs but lacked enforceable definitions of "Meaningful Transformation". | **UPDATE**: Add `VisualStateGraph` and hard transformation requirements. |
| `references/living-motion.md` | Skill `references/` | **YES** | **YES** | **NO (CONFLICT)** | Promoted `CameraRig` subtle continuous zoom (1.00 $\to$ 1.05) as "carrying scene life," which agents abused as a substitute for visual animation. | **REWRITE**: Replace with `references/motion-doctrine.md`. Explicitly ban camera zoom as substitute for animation. |
| `references/voice-director-and-persian-tts.md` | Skill `references/` | **YES** | **YES** | **NO (CONFLICT)** | Hardcoded `style_instruction`: "بدون شتاب و مقتدر" which forced Gemini TTS into an unnaturally slow, ceremonial crawl, dragging video pacing. | **REWRITE**: Replace with `references/voice-doctrine.md`. Mandate natural conversational Persian (130–165 WPM). |
| `references/anti-patterns.md` | Skill `references/` | **YES** | **YES** | **YES** | None. Accurate catalog of historical failures. | **KEEP & EXPAND**: Add S1–S8 slideshow signatures. |
| `references/cinematography.md` | Skill `references/` | **YES** | **YES** | **PARTIAL** | Prescribes camera angles but didn't prevent camera-only motion from faking animation. | **UPDATE**: Subordinate camera strictly to subject consequence. |
| `references/anti-cliche-rules.md` | Skill `references/` | **YES** | **YES** | **YES** | Banned random HUDs, floating particles, and neon clichés. | **KEEP**: Elevate to hard enforcement. |
| `references/visual-critique.md` | Skill `references/` | **YES** | **YES** | **NO (PERMISSIVE)** | Allowed agents to self-evaluate and self-score 9/10 while outputting a static slideshow. | **REWRITE**: Replace with Blind Review Protocol & Hard Fail Conditions. |
| `references/sound-design.md` | Skill `references/` | **YES** | **YES** | **YES** | Multi-track audio and SFX synchronization. | **KEEP**: Enforce frame-accurate SFX alignment. |
| `docs/SHOTBOOK.md` | Mentioned in `SKILL.md` | **NO (BROKEN)** | **NO** | **NO** | Mentioned as required output in Phase 1, but no schema or template was provided in the skill package. | **FIX**: Create standard `SHOTBOOK` template and schema. |
| `scripts/beat_lint.py` | Mentioned in `SKILL.md` | **NO (BROKEN)** | **NO** | **NO** | Mentioned as automated QA check in Phase 4, but file was missing from `scripts/`. | **FIX**: Create executable lint script or replace with `anti_slideshow_audit.py`. |
| `scripts/motion_check.py` | Mentioned in `SKILL.md` | **YES** | **YES** | **YES** | CV-based motion detection script. | **KEEP & REFACTOR**: Update with intentional stillness whitelist. |
| `template/src/camera/CameraRig.tsx` | Skill template | **YES** | **YES** | **NO (HARMFUL)** | Contains naive 1.00 $\to$ 1.05 zoom. Agents copied this and assumed it satisfied "cinematic motion". | **REFACTOR**: Replace with `CameraGrammarRig` requiring motivated moves. |
| `template/src/motion/transitions.tsx` | Skill template | **YES** | **YES** | **NO (HARMFUL)** | Contains generic opacity `fade`. Directly induced slideshow behavior. | **REFACTOR**: Restrict `fade` to emergency; enforce motion-carry. |
| `template/src/motion/WordReveal.tsx` | Skill template | **YES** | **YES** | **NO (HARMFUL)** | Words springing into static cards. Encouraged PowerPoint bullet point behavior. | **DEPRECATE**: Typography must be integrated into world geometry or kinetic transformation. |

---

## 2. Summary of Conflicts Found
1. **Camera Motion vs. Transformation:** `references/living-motion.md` explicitly recommended a 1.00 $\to$ 1.05 camera zoom to "eliminate the static stage look." This directly caused the agent to leave subjects completely stationary and claim that the scene was "animated" because the camera zoomed.
2. **Ceremonial TTS Prompting:** `references/voice-director-and-persian-tts.md` provided a prompt instruction ("بدون شتاب") that told the TTS engine to speak slowly. This directly caused sluggish, draggy speech that ruined the pacing of fresh sessions.
3. **Template Poisoning:** The files inside `template/src/` contained legacy V1-era primitives (`CameraRig.tsx`, `transitions.tsx`, `WordReveal.tsx`) which directly contradicted the v40.1 anti-slideshow rules. When fresh sessions scaffolded from `template/`, they inadvertently inherited PowerPoint-style transitions.
4. **Self-Review Rubber-Stamping:** `references/visual-critique.md` allowed the agent to self-grade its own work using subjective prose, resulting in false PASS declarations.
