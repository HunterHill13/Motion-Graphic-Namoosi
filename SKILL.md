---
name: cinematic-motion-director
description: "AI Cinematic Motion Design Production Engine (Claude Opus 5.5 Calibrated): 15 Canonical Motion Styles (Flat Vector 2D, Shape Morph, Sticker Explainer, Tactile Collage, Isometric 2.5D, Cyberpunk HUD, Liquid Motion, Aurora Glass), Master Frame Cue Sheets (cues.json), Directorial Shotbook Protocol, Typographic Punch Law, Kinematics Library (lib/motion.js), Photographic Plate Engine (lib/image_plates.js), High-Speed Headless Chrome Shutter-Blur Rendering (harness/render.mjs), Procedural 48kHz Stereo Audio Synthesis (mgaudio), and 7-Dimension Adversarial Rubric Review."
---

# cinematic-motion-director

Enterprise autonomous motion-graphics directing engine calibrated against the global gold standard (Claude Opus 5.5 / Buck / Ordinary Folk / Apple Keynote / Pentagram).
Transforms ideas, briefs, profiles, and data into canonical, award-grade motion-design films.

---

## ۱. ارکان بنیادین کارگردانی (The 6 Absolute Directorial Invariants)

هر تصمیم بصری، حرکتی و صوتی باید بدون استثنا از سلسله‌مراتب زیر پیروی کند:

```text
1. NARRATIVE METAPHOR         (ایده با کدام تحول هندسی و استعاره بصری مجسم می‌شود؟)
2. ONE HERO MOVES AT A TIME    (در هر لحظه تنها یک سوژه اصلی حرکت می‌کند؛ حذف شلوغی بصری)
3. CLOSED-FORM PHYSICAL MATH  (انقباض -> پرتاب -> له‌شدگی/کشیدگی برداری -> جهش اورشوت -> استقرار)
4. ELEMENT-DRIVEN TRANSITION  (ترنزیشن با رشد المان، ماسک وایپ یا دگردیسی پیوسته انجام می‌شود)
5. MASTER CUE SYNCHRONIZATION (تصویر و صدا هر دو مستقیماً از شیت فریم مشترک cues.json تغذیه می‌کنند)
6. LIVING END-FRAME HOLD      (ایستایی نمادین لوگو/تایتل به مدت ۰.۸ تا ۱.۲ ثانیه با میکرو-موشن زنده)
```

---

## ۲. خطوط قرمز قطعی کارگردانی و ضد-اسلاید (Hard Invariants)

* **ابطال کامل تله اسلاید متنی (Zero Slide-Deck Fallacy):**
  استفاده از پاراگراف‌های متنی، بولت‌پوینت‌ها، کادرهای توضیحی و اسلایدهای ارائه‌ای مطلقاً ممنوع است. موشن‌گرافیک یک زبان سینمایی-بصری است، نه یک فایل پاورپوینت متحرک.
* **قانون ۱ تا ۳ کلمه مانیومنتال (Typographic Punch Law):**
  تایپوگرافی روی صفحه منحصراً به کلمات ضربه‌ای **حداکثر ۱ تا ۳ واژه‌ای** در لحظات اوج نماها محدود است (مانند: «تحقیقات ژنتیک»، «دقت تشخیصی»، «بیمارستان بقیه‌الله»).
* **ممنوعیت مستطیل خام عکس (Naked Rectangle Image Defect):**
  قرار دادن تصاویر واقعی (پرتره فرد، عکس ساختمان، اسناد، تجهیزات) به صورت مستطیل خام و برش‌نخورده در صحنه مطلقاً ممنوع است. تمام تصاویر باید از طریق موتور `lib/image_plates.js` در قالب یکی از ۳ تکنیک استودیویی پردازش شوند:
  1. **Sticker Explainer (`drawSticker`):** برش نرم، کادر برجسته سفید ۸ تا ۱۲ پیکسل، سایه شناور آمبینت و خطوط لیدر متصل به داده.
  2. **Tactile Collage (`drawCollage`):** کادر قیچی‌خورده سفید، لایه زیرین کاغذ کرافت، نرخ فریم پله‌ای ۱۲ فریم بر ثانیه و جیتر ارگانیک دستی.
  3. **2.5D Isometric Plate (`drawIsometricPlate`):** پروجکشن پرسپکتیو ارتوگرافیک ۳۰ درجه با سایه افتاده موازی.
* **قلاب زیر ۰.۵ ثانیه (Hook in First 0.5s):**
  صحنه هرگز با بیش از ۰.۳ ثانیه تاریکی یا سکون آغاز نمی‌شود. اولین فریم (f0) باید حامل انرژی کینتیک و ورودی انفجاری باشد.
* **فیزیک پیوسته له‌شدگی و کشیدگی (Vector-Aligned Squash & Stretch):**
  تغییر مقیاس المان‌ها متناسب با بردار سرعت لحظه‌ای حرکت چرخانده شده و محاسبه می‌شود (`applySquashStretch`).
* **فرود اورشوت استاندارد:**
  استفاده اجباری از منحنی جهش استاندارد `cubic-bezier(0.34, 1.56, 0.64, 1)` و اسپرینگ فیزیکی (`lib/motion.js`).
* **انطباق فریم‌ها با کلام گوینده (Voice-First Speech-Lock Protocol):**
  تزریق فله‌ای صدای گوینده به عنوان یک فایل ۶۰ ثانیه‌ای در ثانیه ۰.۰ و حدس زدن شماره فریم‌ها مطلقاً ممنوع است (`VOICEOVER_DESYNC_DEFECT`).
  در کلیپ‌های دارای نریشن یا کلام:
  1. صدای هر پرده به طور مستقل توسط `lib/audio/speech_sync.py` سنتز و متادیتای زمانی کلمات استخراج می‌شود.
  2. مدت پرده برابر با طول کلام به اضافه حاشیه تنفس ($\ge 0.5$ ثانیه) محاسبه و به شبکه ضرب‌های موسیقی (`snap_to_grid`) اسنپ می‌گردد.
  3. شیت فریم `cues.json` مستقیماً از روی زمان‌های واقعی کلام تولید شده و فایل `index.html` موظف است تمام کات‌ها و ورودها را بر اساس `cues.frames[...]` هماهنگ سازد؛ هاردکد کردن ثانیه‌ها در جاوااسکریپت ممنوع است.
  4. فایل صوتی مستر نریشن یا قطعات تفکیک‌شده در `audio.py` روی فریم دقیق شروع هر پرده قرار می‌گیرند تا خطای تجمع زمانی به صفر برسد.

---

## ۳. گردش کار گام‌به‌گام تولید (Step-by-Step Production)

### گام ۱: تدوین سناریوی ۴ پرده‌ای (Directorial Shotbook)
پیش از دست زدن به هر کدی، ایجنت باید سناریوی پرده‌ها را در چت استخراج و ثبت کند:

```text
[DIRECTORIAL SHOTBOOK]
- Subject Archetype: [Biography | Place | Tool | Data | Workflow | Abstract]
- Selected Motion Style: [19-paperclip | 06-collage | 01-flat-vector | 08-morph | 03-isometric]
- Hero Visual Metaphor: [تشریح دقیق تحول بصری و هندسی]
- 4-Beat Frame Schedule:
  * Act 1: Hook (f0–f15 / 0.0–0.5s) — ورودی پرانرژی و انفجار فرم آغازین
  * Act 2: Progression (f15–f180 / 0.5–6.0s) — تکامل پیوسته سوژه اصلی با استگر ۲–۴ فریم
  * Act 3: Climax (f180–f225 / 6.0–7.5s) — اوج کینتیک (Shape Wipe یا دگردیسی بزرگ)
  * Act 4: Living Hold (f225–f300 / 7.5–10.0s) — فرود الاستیک لوگو و تنفس ارگانیک (۱ ثانیه)
- Monumental Words (حداکثر ۱ تا ۳ کلمه در هر پرده):
  * Act 1: [کلمه ضربه‌ای ۱]
  * Act 2: [کلمه ضربه‌ای ۲]
  * Act 4: [عنوان نهایی/برند]
```

### گام ۲: تولید شیت فریم و هماهنگی گفتار (`cues.json` و `lib/audio/speech_sync.py`)
در صورت وجود کلام یا نریشن، شیت فریم مستقیماً توسط موتور سنتز و قفل زمانی صدا ساخته می‌شود:
`uv run python lib/audio/speech_sync.py --shotbook shots.json --out cues.json --out-audio-dir public/audio`

تمام فریم‌های شروع، پایان، وایپ و ضربات صوتی در یک فایل JSON متمرکز ثبت می‌شوند:

```json
{
  "fps": 30,
  "bpm": 120,
  "speech_aligned": true,
  "durationFrames": 300,
  "frames": {
    "shot_01_start": 0,
    "shot_01_speech_end": 78,
    "shot_01_wipe": 105,
    "shot_01_end": 120,
    "shot_02_start": 120
  }
}
```

### گام ۳: پیاده‌سازی تصویر و ادغام ماژول‌ها (`demos/<slug>/index.html`)
* بارگذاری شیت فریم مشترک و فراخوانی ماژول‌های حرکتی و تصویری:
  ```html
  <script type="module">
    import { MotionCraft, spring, pop, anticipation, applySquashStretch, clipShapeWipe } from '/lib/motion.js';
    import { ImagePlates } from '/lib/image_plates.js';
    
    // بارگذاری شیت فریم و پیش‌بارگذاری تصاویر با تضمین عدم توقف رندر
    const cues = await fetch('cues.json').then(r => r.json());
    const assets = await ImagePlates.preload({ hero: 'assets/hero.jpg' });
    
    window.renderAt = async (t) => {
      const f = Math.round(t * 30);
      // رندر قطعی فریم بر اساس cues.frames[...] بدون هاردکد کردن زمان‌ها
    };
    
    window.__ready = true; // تنها پس از بارگذاری کامل دارایی‌ها
  </script>
  ```

### گام ۴: سنتز رویه‌ای صدا با پایتون (`demos/<slug>/audio.py`)
سنتز شکل‌موج‌های صوتی ۴۸ کیلوهرتز استریو با `mgaudio`، منطبق بر میلی‌ثانیه‌های شیت فریم و مسترینگ با استاندارد EBU R128 (-14 LUFS).

### گام ۵: رندر با شتاب‌دهنده کروم (`harness/render.mjs`)
اجرای دستور رندر فریم‌به‌فریم با موشن بلور ۴ سمپلی:
`node harness/render.mjs demos/<slug> --mb 4`

### گام ۶: ممیزی ایزوله داور کیفیت (`motion-director-auditor`)
ساب‌ایجنت داور خروجی را در برابر رابریک ۷ معیاره ارزیابی می‌کند. در صورت مشاهده نقایص (`SLIDE_DECK_REGRESSION`, `STIFF_MOTION_DEFECT`, `NAKED_IMAGE_DEFECT`, `VOICEOVER_DESYNC_DEFECT`) کد بلافاصله وارد چرخه اصلاح خودکار می‌شود.

---

## ۴. کاتالوگ سبک‌های استاندارد و نمونه‌های بنچ‌مارک موجود

| # | شناسه سبک | نام و استعاره محوری | موتور پیاده‌سازی | مسیر بنچ‌مارک آماده |
|---|------------|----------------------|------------------|----------------------|
| **01** | `01-flat-vector` | **Flat Vector 2D** (*Popwise*) | SVG / Canvas 2D | `demos/01-flat-vector/` |
| **08** | `08-morph` | **Shape Morph** (*morphe.*) | 240-Vertex Polygon Canvas | `demos/08-morph/` |
| **13** | `19-paperclip` | **Sticker Explainer** (*Stationery*) | Multi-Layer Canvas & SVG | `demos/19-paperclip/` |
| **06** | `06-collage` | **Collage / Cut-out** (*Noggin Quarterly*) | Mixed Media / Stepped 12fps | `demos/06-collage/` |
| **03** | `03-isometric` | **Isometric 2.5D** (*Isopolis*) | Three.js / Canvas Orthographic | الگو در `lib/image_plates.js` |
| **15** | `22-hud` | **Cyberpunk HUD / FUI** (*Kestrel-9*) | SVG FUI + Three.js | فرمول‌بندی براکت‌ها و رادارها |

---

## ۵. کتابخانه‌های پایه پروژه (`lib/`)

1. **`lib/motion.js`:**
   - `bezier(x1, y1, x2, y2)`: درون‌یابی مکعبی بزیر با معکوس‌سازی نیوتن-رافسون.
   - `overshootEase`: منحنی فرود استاندارد `cubic-bezier(0.34, 1.56, 0.64, 1)`.
   - `spring(t, f, z)` / `springV(t, f, z)`: نوسان‌گر هارمونیک میرا (فرود اسپرینگ طبیعی).
   - `pop(t, t0, f, z, amt, pin)`: تغییر مقیاس اسپرینگ همراه با کشیدگی/له‌شدگی متناسب با سرعت و تثبیت در ثانیه pin.
   - `anticipation(t, t0, dur, amount)`: انقباض ۴٪ تا ۱۰٪ در جهت مخالف قبل از شلیک.
   - `applySquashStretch(ctx, x, y, vx, vy, k, drawFn)`: اعمال کشیدگی و له‌شدگی روی زاویه بردار سرعت با حفظ مساحت.
   - `clipShapeWipe(ctx, cx, cy, radius, renderFn)`: ماسک دایره‌ای روی صحنه برای ترنزیشن بدون کات.

2. **`lib/image_plates.js`:**
   - `preload(manifest)`: بارگذاری ناهمگام و دیکود تصاویر با تولید خودکار مونگرام در صورت بروز خطا.
   - `createFallbackPlaceholder(key, w, h)`: ایجاد بوم مونگرام گرادینت با حروف اول کلید برای تضمین عدم توقف رندر.
   - `drawImageCover(ctx, img, dx, dy, dw, dh)`: برش هوشمند مرکز تصویر متناسب با نسبت ابعاد مقصد.
   - `drawSticker(ctx, img, x, y, w, h, options)`: ایجاد استیکر با گوشه‌های گرد، کادر سفید برجسته و سایه نرم.
   - `drawCollage(ctx, img, x, y, w, h, t, options)`: کلاژ مقوایی با لایه کرافت، خطوط قیچی و جیتر دستی ۱۲ فریم.
   - `drawIsometricPlate(ctx, img, x, y, w, h, angle)`: پروجکشن ایزومتریک ۳۰ درجه ارتوگرافیک با سایه افتاده.
