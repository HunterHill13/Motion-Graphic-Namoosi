# 🎬 موتور تولید موشن‌گرافیک سینمایی | AI Cinematic Motion Design Engine
## کالیبراسیون جامع بر اساس بنچ‌مارک جهانی کلاد اوپوس ۵.۵ (`mg-styles-15`)

[![Status](https://img.shields.io/badge/Production%20Status-CANONICAL%20BENCHMARK-00E5FF.svg?style=for-the-badge)](SKILL.md)
[![Skill](https://img.shields.io/badge/Agent%20Skill-cinematic--motion--director-FF6600.svg?style=for-the-badge)](SKILL.md)
[![Renderer](https://img.shields.io/badge/Render%20Engine-Headless%20Chrome%20(GPU)-4285F4.svg?style=for-the-badge)](harness/render.mjs)
[![Audio](https://img.shields.io/badge/Audio%20Engine-Procedural%20mgaudio%2048kHz-10B981.svg?style=for-the-badge)](lib/audio/)
[![Rubric](https://img.shields.io/badge/Quality%20Gate-7--Dimension%20Rubric-8B5CF6.svg?style=for-the-badge)](resources/rubrics/motion-director-rubric.md)

[English](#-english) • [فارسی](#-موتور-تولید-موشن‌گرافیک-سینمایی)

---

## 🎥 پیش‌نمایش مسترهای رندر شده روی سیستم / Master Production Showcases

این آثار به صورت فریم‌به‌فریم با کد خالص و شتاب‌دهنده سخت‌افزاری Chrome GPU و موتور صوتی رویه‌ای پایتون مستقیماً روی سیستم لوکال رندر شده‌اند:

### ۱. مستر وکتور فلت دو بعدی (`FlatVector2D_Master.mp4`)
* **سبک:** `01-flat-vector` (الهام‌گرفته از بنچ‌مارک استودیوهای Buck و Ordinary Folk)
* **استعاره بصری:** حرکت پیوسته یک نقطه کینتیک، ورود پله‌ای کاراکترهای هندسی، ترنزیشن‌های انقباضی Shape Wipe
* **صوت:** ساندترک ریتمیک پاپ سنتز شده به همراه افکت‌های Pop و Impact دقیق روی فریم‌ها (-14.03 LUFS)
* **زمان رندر لوکال:** ۳۰۰ فریم در ۷.۴ ثانیه (۰.۰۲ ثانیه بر فریم)
* **[▶ مشاهده ویدیوی مستر Flat Vector](renders/FlatVector2D_Master.mp4)**

### ۲. مستر دگردیسی پیوسته اشکال (`ShapeMorph_Master.mp4`)
* **سبک:** `08-morph` (الهام‌گرفته از رونمایی‌های Apple Keynote و استودیوی Pentagram)
* **استعاره بصری:** چندضلعی پیوسته ۲۴۰ راسی بازنمونه‌برداری‌شده (`resamplePoly`)، انقباض به کپسول خنثی در ۸ فریم، شکوفایی به ۸ آیکون با درونیابی رنگ در فضای Oklab
* **صوت:** ترک سبک فیوچربیس سنتز شده با دراپ‌های ساب‌باس و رایزرهای متناظر
* **پردازش بصری:** رندر با ۴ سمپل موشن‌بلور شاتر دوربین (`mb=4`)
* **[▶ مشاهده ویدیوی مستر Shape Morph](renders/ShapeMorph_Master.mp4)**

---

## 🏛️ اصول بنیادین شش‌گانه کارگردانی (The 6 Directorial Invariants)

1. **انقراض قطعی اسلایدهای متنی (Zero Slide-Deck Fallacy):**
   * ممنوعیت کامل استفاده از کادرهای متنی، ارائه‌های کارتی، پاراگراف‌ها و بولت‌پوینت‌ها.
   * محدودیت تایپوگرافی به ۱ تا ۳ کلمه مانیومنتال در لحظات کلیدی نماها.
2. **فیزیک حرکتی پیوسته (Closed-Form Physical Math):**
   * انقباض قبل از شلیک (Anticipation) به میزان ۴٪ تا ۱۰٪.
   * له‌شدگی و کشیدگی متناسب با سرعت (Squash & Stretch).
   * اورشوت استاندارد نرم با منحنی `cubic-bezier(0.34, 1.56, 0.64, 1)`.
3. **ترنزیشن‌های المان‌محور (Zero-Cut Transitions):**
   * هیچ برشی به صفحه خالی یا فید ایستا وجود ندارد؛ کلیه جابجایی‌ها با رشد فرم هندسی یا دگردیسی انجام می‌شود.
4. **شیت فریم واحد (`cues.json`):**
   * انطباق میلی‌ثانیه‌ای صدا و تصویر با استفاده از یک جدول فریم متمرکز ۳۰۰ فریمی.
5. **موتور صوتی محاسباتی (`mgaudio`):**
   * سنتز استریو ۴۸ کیلوهرتز و مسترینگ خودکار با استاندارد برودکست جهانی EBU R128 (-14.0 LUFS).
6. **فریم پایانی با تنفس زنده (Living End-Frame Hold):**
   * تثبیت نمادین لوگو/عنوان با میکرو-موشن ارگانیک به مدت ۰.۸ تا ۱.۲ ثانیه.

---

## 🚀 راهنمای سریع اجرا و رندر (Quickstart)

### پیش‌نیازها
* Node.js v18+ و مرورگر Google Chrome
* Python 3.10+ به همراه پکیج‌های صوتی (`soundfile`, `pedalboard`, `pyloudnorm`, `numba`, `matplotlib`)
* ابزار `ffmpeg` بر روی مسیر سیستم (PATH)

### دستورات رندر مستقیم
```bash
# ۱. سنتز فایل صوتی پروژه
python demos/01-flat-vector/audio.py

# ۲. رندر ویدیوی نهایی با مرورگر هدلس کروم و اینکود ffmpeg
node harness/render.mjs demos/01-flat-vector

# ۳. استخراج نماهای ثابت برای کنترل کیفیت بصری
node harness/render.mjs demos/01-flat-vector --stills 0.5,2.0,4.5,6.5,8.5,9.5
```

---

## 📂 ساختار دایرکتوری‌های پروژه

```text
├── demos/                 # پروژه‌های مستقل سبک‌های موشن‌گرافیک (HTML, cues.json, audio.py)
│   ├── 01-flat-vector/    # سبک وکتور فلت دو بعدی
│   └── 08-morph/          # سبک دگردیسی پیوسته اشکال
├── harness/               # رندرر پرسرعت مرورگر کروم هدلس (render.mjs) و صفحه پیش‌نمایش
├── lib/audio/             # موتور پردازش و سنتز صدای رویه‌ای (mgaudio)
├── memory/                # حافظه ماندگار و قواعد فشرده کارگردان ارشد موشن
├── renders/               # خروجی‌های ویدیویی نهایی مستر (.mp4)
├── resources/rubrics/     # سند معیارهای ممیزی ۷ معیاره کیفیت
├── AGENTS.md              # راهنمای سطح صفر آنبوردینگ هوش مصنوعی
└── SKILL.md               # مشخصات فنی و استانداردنامه اسکیل تخصصی
```

---

## 🇺🇸 English

### Autonomous Motion Design Production Engine (Claude Opus 5.5 Calibrated)
An enterprise-grade motion design system replacing legacy text-slide presentations with frame-accurate, physically motivated 2D vector animation, continuous vertex morphing, procedural 48kHz sound design, and sub-frame shutter-blur Chrome rendering.
