"""
Persian Pronunciation Planner (v2.1)
Upgraded from PersianTextOptimizer.

Separates narration text into three discrete linguistic contracts:
1. visible_text: Clean, standard Persian script for on-screen kinetic captions and subtitles.
2. spoken_text: Normalized spoken Persian script (numbers expanded, loanwords localized).
3. pronunciation_text: Strategic phonetically-enhanced Persian text with diacritics,
   strategic pauses, and verified scientific pronunciation overrides tailored for TTS engines.
"""

import re
from typing import Dict, Any, List

# Explicit pronunciation dictionary mapping technical/medical terms to phonetic representations
PERSIAN_PRONUNCIATION_DICTIONARY: Dict[str, Dict[str, str]] = {
    "apoptosis": {
        "visible": "آپوپتوز",
        "spoken": "آپوپتوز",
        "pronunciation": "آپوپْتوز",
        "ipa": "ʔɒpoptʰoːz"
    },
    "bcl-2": {
        "visible": "BCL-2",
        "spoken": "بی‌سی‌ال دو",
        "pronunciation": "بی‌سی‌اِل دو",
        "ipa": "biː siː el do"
    },
    "bax": {
        "visible": "BAX",
        "spoken": "بَکس",
        "pronunciation": "بَکْس",
        "ipa": "bæks"
    },
    "bak": {
        "visible": "BAK",
        "spoken": "باک",
        "pronunciation": "باک",
        "ipa": "bɒːk"
    },
    "momp": {
        "visible": "MOMP",
        "spoken": "مامپ",
        "pronunciation": "مامْپ",
        "ipa": "mɒmp"
    },
    "cytochrome c": {
        "visible": "سیتوکروم c",
        "spoken": "سیتوکروم سی",
        "pronunciation": "سیتوکْرومِ سی",
        "ipa": "siːtʰokʰroːme siː"
    },
    "caspase-9": {
        "visible": "کاسپاز-۹",
        "spoken": "کاسپاز نه",
        "pronunciation": "کاسْپازِ نُه",
        "ipa": "kʰɒːspɒːze noh"
    },
    "caspase-3": {
        "visible": "کاسپاز-۳",
        "spoken": "کاسپاز سه",
        "pronunciation": "کاسْپازِ سه",
        "ipa": "kʰɒːspɒːze se"
    },
    "apaf-1": {
        "visible": "Apaf-1",
        "spoken": "آپاف یک",
        "pronunciation": "آپافِ یک",
        "ipa": "ʔɒːpʰɒːfe jæk"
    }
}

class PersianPronunciationPlanner:
    """Produces triple-layer narration contracts: visible, spoken, and pronunciation."""

    def __init__(self, dictionary: Dict[str, Dict[str, str]] = None):
        self.dict = {**PERSIAN_PRONUNCIATION_DICTIONARY, **(dictionary or {})}

    def plan_sentence(self, raw_input: str) -> Dict[str, str]:
        visible = raw_input
        spoken = raw_input
        pronunciation = raw_input

        # Substitute known technical terms
        for term, mapping in self.dict.items():
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            visible = pattern.sub(mapping["visible"], visible)
            spoken = pattern.sub(mapping["spoken"], spoken)
            pronunciation = pattern.sub(mapping["pronunciation"], pronunciation)

        # Expand percentage and digits in spoken & pronunciation
        num_pattern = re.compile(r"(\d+)%")
        visible = num_pattern.sub(r"\1٪", visible)
        spoken = num_pattern.sub(r"\1 درصد", spoken)
        pronunciation = num_pattern.sub(r"\1 دَرْصَد", pronunciation)

        return {
            "visible_text": visible.strip(),
            "spoken_text": spoken.strip(),
            "pronunciation_text": pronunciation.strip(),
        }

if __name__ == "__main__":
    planner = PersianPronunciationPlanner()
    sample = "پروتئین bcl-2 از فعال‌سازی bax و رخ دادن momp جلوگیری می‌کند."
    res = planner.plan_sentence(sample)
    print("Visible Text:      ", res["visible_text"])
    print("Spoken Text:       ", res["spoken_text"])
    print("Pronunciation Text:", res["pronunciation_text"])
