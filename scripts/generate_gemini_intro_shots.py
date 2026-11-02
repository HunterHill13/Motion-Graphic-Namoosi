#!/usr/bin/env python3
"""
Generate Gemini Audio Voiceover for the 4 Acts of SkillIntroShowreel.
Uses synthesize_gemini_tts.py with model hierarchy and voice Puck.
Converts generated WAV to MP3 and replaces public/audio/intro_shot_{1..4}.mp3.
"""

import os
import sys
import subprocess
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from synthesize_gemini_tts import synthesize_narration

SHOTS = [
    {
        "id": "intro_shot_1",
        "text": "به نسل جدید موشن‌گرافیک سینمایی خوش آمدید؛ پیوستگی بی‌نقص در تراز کلاد اوپوس پنج و نیم."
    },
    {
        "id": "intro_shot_2",
        "text": "با تبدیل واقعی بردارها، حرکت دوربین شش درجه آزادی و فیزیک اسپرینگ استودیویی."
    },
    {
        "id": "intro_shot_3",
        "text": "کنسول نرم‌افزاری دو و نیم بعدی با پایش زنده تله‌متری و تایپوگرافی رسمی یکان‌بخ."
    },
    {
        "id": "intro_shot_4",
        "text": "کالیبراسیون صد در صد و استانداردهای طلایی؛ آماده برای تحول در تولید محتوای هوش مصنوعی."
    }
]

def main():
    output_dir = Path("public/audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    voice = "Puck"
    
    print("=" * 60)
    print("GENERATING GEMINI AUDIO NARRATION FOR 4 ACTS")
    print(f"Voice: {voice} (Puck - Male)")
    print("=" * 60)
    
    results = []
    for shot in SHOTS:
        print(f"\n[SYNTHESIZING] {shot['id']}: \"{shot['text']}\"")
        res = synthesize_narration(
            text=shot["text"],
            voice=voice,
            video_id=shot["id"],
            output_dir=output_dir,
            force_fresh=True
        )
        wav_path = Path(res["output_path"])
        mp3_path = output_dir / f"{shot['id']}.mp3"
        
        # Clean audio conversion: The WAV is already surgically stripped of Gemini trailing pops
        audio_filter = "afade=t=in:ss=0:d=0.03,apad=pad_dur=0.10"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(wav_path),
            "-af", audio_filter,
            "-codec:a", "libmp3lame",
            "-qscale:a", "2",
            str(mp3_path)
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"  [OK] Converted to MP3: {mp3_path} ({mp3_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"  [WARN] ffmpeg conversion failed: {e}. Keeping WAV.")
            
        print(f"  Model Used: {res['actual_model']}")
        print(f"  Duration: {res['audio_duration']}s")
        results.append(res)
        
    print("\n" + "=" * 60)
    print("ALL 4 ACTS SYNTHESIZED WITH GEMINI AUDIO SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
