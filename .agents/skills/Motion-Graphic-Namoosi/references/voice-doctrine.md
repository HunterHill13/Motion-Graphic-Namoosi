# Single Authoritative Voice Doctrine

## 1. Persona & Delivery Philosophy
The spoken voiceover must embody:
> **A highly skilled Persian narrator delivering a punchy, energetic, modern promotional/educational film with confidence, fluency, and warmth.**

It must NEVER sound like:
- ❌ An antiquated ceremonial cleric reading a religious parchment.
- ❌ An artificially slow, robotic voice crawling at $< 115$ words per minute.
- ❌ A lifeless bureaucrat reciting legal clauses with dead, uniform cadence.
- ❌ A melodramatic stage actor overacting with theatrical breathiness.

**Target Delivery:**
> **Professional + Energetic + Fluent + Confident + Natural Persian.**

---

## 2. Mandatory Voice Selection Gate (`VOICE_SELECTION_GATE`)

Before generating narration, timing, or beginning visual Remotion production, the director **MUST** prompt the user to explicitly select an approved Gemini narration voice (unless already answered in the active session):

### Approved Voices:
* **🎙️ Puck (پوک):** مرد — رسمی، پرانرژی، مدرن و پویا (مناسب کلیپ‌های تبلیغاتی، علمی و پروموشن)
* **🎙️ Callirrhoe (کالیرو):** زن — طبیعی، آرام، صمیمی و روان (مناسب محتوای آموزشی، فاخر و پروموشن)

### Mandatory Persian Prompt:
> «قبل از شروع ساخت ویدیو، لطفاً صدای راوی را انتخاب کنید:
> 
> **🎙️ گزینه‌های مصوب (Google Gemini Multimodal Audio):**  
> 1. **Puck (پوک)** — مرد: رسمی، پرانرژی، مدرن و پویا  
> 2. **Callirrhoe (کالیرو)** — زن: طبیعی، آرام، صمیمی و روان  
> 
> کدام را انتخاب می‌کنید؟»

---

## 3. Quota-Aware Model Hierarchy

* **Priority 1 (Default / Highest Quality):** `gemini-3.8-flash-tts`
* **Priority 2 (First Quota Fallback):** `gemini-3.8-flash-lite-tts`
* **Priority 3 (Final Quota Fallback):** `gemini-3.1-flash-tts-preview`

### Zero Speculative Probing Doctrine:
* **NEVER** probe candidate models in advance.
* Only fall back if an authentic quota failure occurs (`is_authentic_quota_failure()`).
* Non-quota failures (e.g. 401 Unauthorized, 400 Bad Request, network errors) fail immediately without switching models.

---

## 4. Default Narration Style Mandate

The production prompt for Gemini Persian narration is:

```text
«رسمی و پرانرژی، مناسب کلیپ تبلیغاتی؛
طبیعی، روان و محاوره‌ای،
با ریتم مناسب و confident delivery،
بدون لحن گویندگی خشک، رسمیِ سنگین یا اغراق‌آمیز.»
```

---

## 5. Preflight Sample Protocol

1. Synthesize exactly ONE 10–15s sample using canonical preflight text:
   `«این ویدیو برای معرفی نسل نوین سامانه‌های هوش مصنوعی و ساخت موشن‌گرافیک پیشرفته تقدیم می‌شود.»`
2. Present sample to user for approval.
3. Upon approval, synthesize the final full-video narration in ONE single request.

---

## 6. One Video = One TTS Request

* Entire script synthesized in ONE single call.
* No scene-by-scene splitting.
* Long text exception (>4000 characters) cleanly chunked at sentence boundaries.
