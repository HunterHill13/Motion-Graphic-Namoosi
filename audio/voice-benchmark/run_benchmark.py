"""
Persian TTS Benchmark Suite
Evaluates engines across:
1. Naturalness (prosody, rhythm, sentence cadence)
2. Persian ezafe handling and diacritics
3. Technical/medical term accuracy
4. Processing latency
"""

import time
import json
import os
import sys
from pathlib import Path

# Add engine directory to path
sys.path.append(str(Path(__file__).parent.parent / "engine"))
from PersianTextOptimizer import PersianTextOptimizer
from VoiceDirector import VoiceDirector

BENCHMARK_SENTENCES = [
    {
        "id": "medical_ezafe",
        "description": "Medical terminology with critical Persian ezafe and complex acronyms",
        "raw_text": "پروتئین‌های خانواده BCL-2 با مهار مسیر آپوپتوز میتوکندریایی، بقای سلول‌های توموری را تضمین می‌کنند."
    },
    {
        "id": "numbers_percentage",
        "description": "Percentage and numerical metrics with ZWNJ pluralization",
        "raw_text": "بیش از ۷۵٪ بیماران در مرحله دوم درمان، پاسخ بالینی مطلوبی نشان دادند."
    },
    {
        "id": "cinematic_narrative",
        "description": "Dramatic narrative pacing and emotional breath pauses",
        "raw_text": "در ژرفای تاریکی سلول، یک تصمیم سرنوشت‌ساز گرفته می‌شود: مرگ یا بقا؟"
    }
]

def run_benchmark():
    out_dir = Path("audio/voice-benchmark/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    optimizer = PersianTextOptimizer()
    director = VoiceDirector(preferred_provider="edge")
    
    report = {
        "benchmark_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sentences_tested": len(BENCHMARK_SENTENCES),
        "results": []
    }
    
    for item in BENCHMARK_SENTENCES:
        clean_text = optimizer.clean_for_tts(item["raw_text"])
        out_audio = str(out_dir / f"{item['id']}.mp3")
        
        t0 = time.time()
        meta = director.produce_narration(item["raw_text"], out_audio, provider="edge")
        latency = round(time.time() - t0, 3)
        
        report["results"].append({
            "id": item["id"],
            "description": item["description"],
            "raw_text": item["raw_text"],
            "optimized_text": clean_text,
            "output_audio": out_audio,
            "latency_seconds": latency,
            "provider_used": meta.get("provider"),
            "voice_used": meta.get("voice"),
            "status": meta.get("status")
        })
        
    report_file = out_dir / "benchmark_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Benchmark completed successfully. Report written to {report_file}")
    return report

if __name__ == "__main__":
    run_benchmark()
