# Persian TTS Production Protocol & Prosody Engineering (v3.2)

---

## 1. Engine Routing Hierarchy
1. **Primary Production Candidate:** Google Gemini 2.5 Pro TTS (`fa-IR` Tehran Dialect) with emotional prosody prompt injection.
2. **Calibrated Local Production Engine:** Calibrated Edge-TTS (`fa-IR-FaridNeural` at rate `+7%`, pitch `-1Hz`) with phonetic dictionary mapping.
3. **Offline Neural Clone (Fallback):** Pocket-TTS Farsi v2 ONNX engine (`mehdi-hf/pocket-tts-farsi-v2`).
4. **Experimental Integration:** NotebookLM Audio Overview (Architecture stub for non-blocking future expansion).

---

## 2. Natural Iranian Delivery Directive Prompt
> "این متن را مانند یک گوینده مستند علمی حرفه‌ای ایرانی بخوان. فارسی معیار طبیعی ایران، نه فارسی دری. لحن پرانرژی، گرم و مطمئن باشد. جملات را خشک و یکنواخت نخوان. روی واژه‌های کلیدی تأکید طبیعی داشته باش و بین ایده‌ها مکث کوتاه داشته باش. اصطلاحات زیست‌پزشکی را شمرده و مسلط بیان کن."

---

## 3. Targeted Diacritic Strategy
- Blind diacritization is strictly prohibited.
- Subtitles display clean, unvoweled Dubai Persian font.
- Speech inputs receive vowels strictly to prevent incorrect syllabic stress (e.g. `آپوپْتوز` vs. default flat reading).
