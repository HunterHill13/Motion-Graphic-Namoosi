# Mandatory Voice Selection & Two-Stage TTS Protocol (Edge Preview + Gemini Final)

## 1. Two-Stage Production Architecture

```text
USER REQUEST
     ↓
SCRIPT & STORYBOARD
     ↓
VOICE SELECTION (Puck vs Callirrhoe)
     ↓
STAGE 1: EDGE-TTS PREVIEW (Zero Gemini Quota)
     ↓
FULL REMOTION MOTION-GRAPHICS RENDER
     ↓
USER REVIEWS PREVIEW VIDEO
     ↓
┌─────────────────────────────────┐
│ User Approval Decision?         │
└────────────────┬────────────────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
    REVISION            APPROVE
       │                   │
  Modify motion            ▼
  Re-render Preview     STAGE 2: GEMINI FINAL TTS
  (Gemini BLOCKED)         │
                           ├─► Priority 1: gemini-3.8-flash-tts
                           ├─► Priority 2: gemini-3.8-flash-lite-tts
                           └─► Priority 3: gemini-3.1-flash-tts-preview
                           │
                        MEASURE ACTUAL GEMINI DURATION
                           │
                        RECALCULATE FINAL TIMING
                           │
                        FINAL MASTER RENDER
```

---

## 2. Mandatory Voice Selection Gate (`VOICE_SELECTION_GATE`)

Before generating preview or final video, the director **MUST** prompt the user to explicitly select the target Gemini narration voice (unless already answered in the active session):

### 🎙️ صداهای مصوب Gemini:
1. **Puck (پوک)** — مردانه: رسمی، پرانرژی، مدرن و پویا
2. **Callirrhoe (کالیرو)** — زنانه: طبیعی، آرام، صمیمی و روان

---

## 3. Stage 1: Edge-TTS Preview (Motion Validation)

- **Role:** Purely for validating motion graphics, pacing, camera choreography, transitions, and composition.
- **Provider:** Microsoft Edge-TTS (`fa-IR-FaridNeural`).
- **Quota Impact:** **ZERO Gemini requests. ZERO Gemini quota.**
- **Artifact:** `public/audio/preview/edge/{video_id}_preview_voice.wav` -> `renders/preview/{video_id}_preview_edge.mp4`.
- **Motion-Only Optimization:** If the user requests motion adjustments without altering narration script, the existing Edge-TTS audio is reused instantly with 0 TTS calls.

---

## 4. User Review Presentation Template

Upon completing the Preview render, the agent stops and presents:

> «🎬 **Preview ویدیو آماده شد.**
> 
> این نسخه با **Microsoft Edge-TTS** تولید شده و صرفاً برای بررسی:
> • کیفیت موشن گرافیک (Motion Design)  
> • ریتم و تایمینگ (Timing & Pacing)  
> • پیوستگی و ترنزیشن‌ها (Transitions & Continuity)  
> • ترکیب‌بندی بصری (Composition & Layout)  
> 
> است.
> 
> *صدای نهایی هنوز تولید نشده و هیچ سهمیه Gemini مصرف نشده است.*  
> 
> اگر موشن گرافیک و ساختار کلی مورد تأیید است، لطفاً بنویسید:  
> **«تأیید»**  
> تا نریشن نهایی با Gemini TTS تولید و تایمینگ قطعی رندر شود.»

---

## 5. Stage 2: Gemini Final Production & Timing Recalibration

Only when the user provides explicit approval:
1. Gemini TTS synthesizes the full video script in **ONE monolithic request**.
2. Strict fallback chain: `gemini-3.8-flash-tts` -> `gemini-3.8-flash-lite-tts` -> `gemini-3.1-flash-tts-preview` (Quota failure only).
3. **Actual Duration Truth:** Audio duration is measured from the resulting Gemini WAV file.
4. Total frames and scene boundaries are recalibrated to the exact Gemini duration (`is_final = True`).
5. Master video is rendered to `renders/final/{video_id}_final_gemini.mp4`.
