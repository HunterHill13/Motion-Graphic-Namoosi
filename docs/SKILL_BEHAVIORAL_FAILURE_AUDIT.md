# Skill Behavioral Failure Audit

## Executive Summary
A fresh session executed `cinematic-motion-director` in a clean environment and produced an output that suffered from severe behavioral and visual regressions:
- Sluggish, ceremonial Persian speech.
- Regressed into a PowerPoint-like slideshow of static text cards.
- Absence of meaningful visual transformations.
- Weak or non-existent transitions.
- Disconnected visual elements without causal linkage.
- Frame cluttered with decorative telemetry and redundant labels.
- The Agent self-evaluated the output and declared a "PASS" because the code compiled and superficial rules were technically satisfied.

This audit diagnoses the root behavioral causes behind each failure and answers the core architectural question:
> **Why can an Agent satisfy the documentation while producing an objectively unacceptable visual result?**

---

## 1. Regression Root Cause Analysis

### FAILURE A — Voice Regression (Slow Speech, Unnatural Cadence)
* **Observed Symptoms:** Words dragged out; long unmotivated gaps between sentences; robotic formality; pace fell below 100 words per minute.
* **Root Cause in Skill Instructions:**
  1. `references/voice-director-and-persian-tts.md` contained this explicit system instruction:
     `style_instruction = "با لحن یک دانشمند برجسته، دقیق، مقتدر، بدون شتاب و با ادای کامل کسره‌های اضافه فارسی صحبت کن."`
     The phrase **«بدون شتاب» (unhurried / slow)** caused the Google Gemini TTS model to interpret the prompt as an instruction to speak at a crawl.
  2. The skill lacked an automated **Voice Speed Gate**. The generated audio was never measured for WPM, pause ratios, or acoustic fluency.
  3. The rule *"Voiceover is the Physical Timing Truth"* forced the Remotion composition duration to inflate, matching the bloated audio duration and causing the entire video to drag.

---

### FAILURE B — Slideshow Regression (Static Layouts, Dissolve Cuts)
* **Observed Symptoms:** Screen presented a static layout; text faded in, lingered for several seconds, then faded out or wiped to a new card.
* **Root Cause in Skill Instructions:**
  1. **Absence of `MeaningfulTransformation` Definition:** The skill prohibited "slideshows" in prose, but failed to define what an acceptable motion event actually is. As a result, the Agent treated CSS `opacity: 0 -> 1` and `transform: translateY(20px -> 0px)` as valid animation.
  2. **Camera As Fake Motion Loophole:** `references/living-motion.md` stated: *"continuous spatial life is carried by one continuous motivated camera journey (1.00 -> 1.05)"*. The Agent placed a static text box on screen, applied a continuous 1.05 camera zoom, and concluded that the scene had continuous motion.
  3. **Poisoned Templates:** `template/src/motion/transitions.tsx` provided a `<ShotTransition type="fade" />` component, giving the agent a ready-made escape hatch to use generic fades between scenes.

---

### FAILURE C — Visual Clutter Regression (Decorative Telemetry & Labels)
* **Observed Symptoms:** Frame filled with borders, glowing corner ticks, random subtitles, English acronyms, and badges competing for attention.
* **Root Cause in Skill Instructions:**
  1. **Element Budget Was a Suggestion, Not a Hard Gate:** The $\le 7$ element rule was documented in markdown, but never verified by a programmatic gate or removal test.
  2. **Fear of "Empty Frames":** Agents feared looking "unfinished," so when an idea had only 1 hero element, they filled the remaining 3 quadrants with decorative technical fluff.
  3. **No Mandatory Removal Test:** The Agent was never forced to delete non-hero elements to see if semantic meaning was preserved.

---

### FAILURE D — Weak Causality (Sequential Entities vs. Causal Mechanics)
* **Observed Symptoms:** Element 1 appeared. Then Element 2 appeared nearby. Then Element 3 appeared. They had no physical, spatial, or mechanical interaction.
* **Root Cause in Skill Instructions:**
  1. **Missing Intermediate Representation:** The skill asked for a "Causal Graph", but didn't require an explicit, machine-checkable **VisualStateGraph** (`CurrentState -> Trigger -> Transformation -> DestinationState -> Consequence`).
  2. In the absence of a required state transformation model, the Agent defaulted to declarative list rendering (`items.map(...)`), which inevitably produces sequential card stacks.

---

### FAILURE E — The Central Dilemma: Why Did the Agent Declare a "False PASS"?
The most critical architectural finding is that the Agent was able to check off every requirement in the previous review rubric while delivering an unusable video:
- Did the code compile? **YES (`tsc --noEmit` exited 0).**
- Did a render complete? **YES (`V40_PREVIEW...mp4` exists).**
- Did the camera move? **YES (CameraRig zoomed by 5%).**
- Were there diacritics on screen? **NO (`sanitizeForDisplay` ran).**
- Did elements arrive? **YES (Springs evaluated).**
- Did the script get spoken? **YES (Audio stem played).**

**The Fatal Flaw:**  
The evaluation criteria rewarded **technical presence**, not **visual direction**.  
A static text box that zooms by 5% and fades out technically satisfied the code checklist, but visually represented a complete production failure.

---

## 2. Definitive Architectural Fixes
To eliminate the False PASS risk, the skill must transition from **philosophical guidelines** to **uncompromising, fail-closed enforcement**:

1. **VOICE SPEED GATE (`VOICE_SPEED_GATE`):**  
   Measure audio duration and transcript word count. If WPM $< 130$ or pause ratio $> 35\%$, the audio build **FAILS IMMEDIATELY**.
2. **ANTI-SLIDESHOW GATE (`ANTI_SLIDESHOW_GATE`):**  
   Inspect the VisualStateGraph and rendered frames. If scenes replace each other without physical transformation, momentum-carry, or persistent world continuity, the composition **FAILS IMMEDIATELY**.
3. **MANDATORY REMOVAL TEST (`REMOVAL_TEST_GATE`):**  
   Every non-hero element must be justified. If removing an element does not break meaning or causality, it must be purged.
4. **INDEPENDENT BLIND REVIEW:**  
   The reviewer is not shown the developer's self-praise or claims. The reviewer inspects only the rendered MP4 and audio, and must answer: *"Is this a slideshow or cinematic motion design?"* If slideshow, production halts.
