# Cinematic Motion Director (اسکیل موشن گرافیک سینمایی)

> **Autonomous AI Cinematic Video Production Pipeline for Remotion & React**  
> *Certified for Google Antigravity, Claude Code, Cursor, Windsurf, and LLM Agent Workspaces.*

---

## 🌟 ویژگی‌های برجسته (Key Highlights)

- **۹ آرکتایپ بصری سینمایی (9 Master Archetypes):**
  - Dark Graphite Tech (تکنولوژی تاریک و مینیمال)
  - Continuous UI Morph (مورفینگ پیوسته رابط کاربری)
  - Quantum Bio Deep-Z (زیست‌پزشکی کوانتومی و سلولی در عمق Z)
  - Kinetic Architectural Typo (تایپوگرافی معماری و مقیاس‌های سنگین)
  - Bento Grid SaaS (شبکه فضایی و ماژولار نرم‌افزاری)
  - FinTech Trading & Candlestick (داده‌های مالی و امواج نقدینگی)
  - Stop-Motion Paper Cutout (کاغذ دست‌ساز با نرخ فریم استپ‌شده)
  - Technical Blueprint CAD (نقشه فنی مهندسی و خطوط ابعادی)
  - Neo-Brutalist High-Contrast (بلوک‌های اسیدی پرانرژی و زاویه‌دار)

- **استاندارد کیفی Claude Opus 5.5 Motion:**
  - فیزیک اسپرینگ کالیبره‌شده اختصاصی برای هر متریال (`mass`, `stiffness`, `damping`).
  - ریتم سه‌گانه هر صحنه (۱۸٪ ورود پرانرژی، ۶۸٪ شناوری و ریزحرکات پویا، ۱۴٪ ترنزیشن خروج).
  - شبکه ضرب‌آهنگ ریاضی (Mathematical Beat-Grid Snapping) هماهنگ با تمپو موسیقی (BPM).
  - فضای رنگی ادراکی **OKLCH** جهت حذف نقاط مرده خاکستری در گرادینت‌ها.

- **تایپوگرافی جنبشی ایمن زبان فارسی (`PersianKineticText`):**
  - انیمیشن کلمه به کلمه با مسک پرده‌ای (`clipPath`) و چرخش سه‌بعدی بدون گسستگی حروف خوشنویسی.

- **بوم باز بدون جعبه (Open-Canvas Zero-Box Doctrine):**
  - حذف کامل کادرهای مستطیلی اسلایدی و حاشیه‌های اضافی.
  - حذف واترمارک‌ها و برچسب‌های شلوغ گوشه تصویر؛ تمرکز ۱۰۰٪ روی مفهوم محوری.

- **کارگردانی ترنزیشن‌های پویا (Dynamic Camera & Scene Transitions):**
  - ۵ الگوی ترنزیشن هدفمند (Whip Pan, Vertical Crane, Deep-Z Zoom, Anchor Morph, Kinetic Disperse).

- **موتور صوت دومرحله‌ای (Two-Stage Audio Pipeline):**
  - پیش‌نمایش سریع صوتی با Microsoft Edge-TTS بدون نیاز به API Key.
  - خروجی نهایی استودیویی با Google Gemini Multimodal Audio.

---

## 🚀 راهنمای نصب و راه‌اندازی (Installation Guide)

### ۱. نصب در Google Antigravity / Gemini CLI
پوشه `cinematic-motion-director` را در یکی از مسیرهای زیر قرار دهید:
- **به صورت سراسری (برای همه پروژه‌ها):**
  ```text
  ~/.gemini/config/skills/cinematic-motion-director
  ```
  *(در ویندوز: `C:\Users\<YourUser>\.gemini\config\skills\cinematic-motion-director`)*
- **به صورت محلی در یک پروژه:**
  ```text
  <YourProjectFolder>/.agents/skills/cinematic-motion-director
  ```

### ۲. نصب در Claude Code
پوشه را در مسیر اسکیل‌های Claude Code قرار دهید:
```text
~/.claude/skills/cinematic-motion-director
```

### ۳. نصب در Cursor / Windsurf / VS Code
پوشه را در مسیر ورک‌اسپیس خود در پوشه `.agents/skills/` کپی کنید.

---

## 🎬 نحوه استفاده (Usage)

کافی است در چت هوش مصنوعی، موضوع و ساختار ویدیوی مورد نظر خود را درخواست کنید:

### نمونه درخواست‌های فارسی:
> «یک موشن گرافیک سینمایی ۳۰ ثانیه‌ای درباره عملکرد واکسن‌های mRNA با تم Quantum Bio Deep-Z بساز.»

> «برای معرفی سامانه هوش مصنوعی پزشکی، یک ویدیوی عمودی ۹:۱۶ اینستاگرامی با تم Dark Graphite Tech بساز.»

### Example English Prompts:
> "Create a 45-second kinetic typography explainer video about agentic workflows using the Kinetic Architectural Typo archetype."

---

## 🛠 تست و اعتبارسنجی مستقل (Stand-alone Validation)

درون پوشه `template/` اسکیل، یک پروژه کامل Remotion TypeScript قرار دارد. برای تست و اجرای محلی:

```bash
cd template
npm install
npx tsx tests/test_claude_motion_standards.ts
npm start
```

---

## 📂 ساختار بسته (Package Structure)

```text
cinematic-motion-director/
├── SKILL.md                  # دستورالعمل جامع مغز هوش مصنوعی
├── README.md                 # راهنمای نصب و معرفی اسکیل
├── schemas/                  # اسکیماهای اعتبارسنجی (VisualStateGraph)
├── scripts/                  # اسکریپت‌های تبدیل صوت Edge-TTS و پایپ‌لاین
├── templates/                # قالب‌های Beat Sheet، Storyboard و QC
├── workflows/                # ورک‌فلوهای عملیاتی (Mode A تا Mode E)
├── references/               # مراجع طراحی، رنگ‌ها و دستور زبان موشن
├── assets/                   # فونت‌های استاندارد و تصاویر راهنما
└── template/                 # پروژه پایه قابل اجرای Remotion (TypeScript)
    ├── package.json
    ├── remotion.config.ts
    ├── src/                  # موتور رندر، استیج، کمرا، تایپوگرافی و تمپلیت‌ها
    ├── public/               # است‌های صوتی و فونت‌ها
    └── tests/                # تست‌های ۹ گیت کیفی و AST
```

**License:** MIT  
**Author:** Deepmind & Cinematic Motion Graphics Research Team
