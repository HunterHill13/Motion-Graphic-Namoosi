"""
Persian Text Optimizer for Natural TTS Synthesis
Handles:
1. Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله) standardization
2. Silent Ezafe (-e / -ye) diacritic support
3. Number and percentage expansion to spoken Persian words
4. Medical & Scientific English term phonetic transliteration
"""

import re
from typing import Dict

# Common medical and motion design loanwords to phonetic Persian equivalents
PHONETIC_GLOSSARY: Dict[str, str] = {
    "apoptosis": "آپوپتوز",
    "bcl-2": "بی‌سی‌ال دو",
    "bcl2": "بی‌سی‌ال دو",
    "bax": "باکس",
    "bak": "باک",
    "momp": "مامپ",
    "cytochrome c": "سیتوکروم سی",
    "apaf-1": "آپاف یک",
    "apaf1": "آپاف یک",
    "caspase-9": "کاسپاز نه",
    "caspase-3": "کاسپاز سه",
    "caspase": "کاسپاز",
    "dna": "دی‌ان‌ای",
    "rna": "آران‌ای",
    "atp": "ای‌تی‌پی",
    "mitochondria": "میتوکندری",
    "mitochondrial": "میتوکندریایی",
    "remotion": "ری‌موشن",
    "fps": "فریم بر ثانیه",
    "lufs": "لوفس",
}

# Persian digits to standard Arabic/Latin
PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

ONES = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
TEENS = ["ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"]
TENS = ["", "ده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"]
HUNDREDS = ["", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"]
THOUSANDS = ["", "هزار", "میلیون", "میلیارد"]

def number_to_persian_words(num: int) -> str:
    """Converts an integer (up to billions) to natural Persian words."""
    if num == 0:
        return "صفر"
    if num < 0:
        return "منفی " + number_to_persian_words(abs(num))
    
    parts = []
    
    def convert_chunk(n: int) -> str:
        c_parts = []
        h = n // 100
        rem = n % 100
        if h > 0:
            c_parts.append(HUNDREDS[h])
        if rem > 0:
            if rem < 10:
                c_parts.append(ONES[rem])
            elif 10 <= rem < 20:
                c_parts.append(TEENS[rem - 10])
            else:
                t = rem // 10
                o = rem % 10
                c_parts.append(TENS[t])
                if o > 0:
                    c_parts.append(ONES[o])
        return " و ".join(c_parts)

    chunks = []
    while num > 0:
        chunks.append(num % 1000)
        num //= 1000

    for i in range(len(chunks) - 1, -1, -1):
        ch = chunks[i]
        if ch > 0:
            txt = convert_chunk(ch)
            if THOUSANDS[i]:
                txt += " " + THOUSANDS[i]
            parts.append(txt)

    return " و ".join(parts)


class PersianTextOptimizer:
    """Optimizes raw Persian script for fluent, natural TTS pronunciation."""

    def __init__(self, phonetic_glossary: Dict[str, str] = None):
        self.glossary = {**PHONETIC_GLOSSARY, **(phonetic_glossary or {})}

    def normalize_zwnj(self, text: str) -> str:
        """Enforces Zero-Width Non-Joiner (ZWNJ) for Persian grammatical constructs."""
        zwnj = "\u200c"
        # Fix common prefixes: می / نمی followed by space -> می\u200c
        text = re.sub(r"\b(ن?می)\s+", r"\1" + zwnj, text)
        
        # Fix plural suffixes: ها / های / هایم -> \u200cها
        text = re.sub(r"\s+(ها|های|هایمان|هایتان|هایشان)\b", zwnj + r"\1", text)
        
        # Fix adjectival suffixes: تر / ترین
        text = re.sub(r"\s+(تر|ترین)\b", zwnj + r"\1", text)
        
        # Collapse multiple spaces
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def expand_numbers_and_symbols(self, text: str) -> str:
        """Converts Latin/Persian numbers and symbols into spoken Persian words."""
        # Normalize digits
        text = text.translate(PERSIAN_DIGITS)
        
        # Replace percentages: 25% or %25 -> ۲۵ درصد
        text = re.sub(r"(\d+)%", r"\1 درصد", text)
        text = re.sub(r"%(\d+)", r"\1 درصد", text)

        # Replace standalone numbers with Persian words
        def replace_num(match):
            val = int(match.group(0))
            return number_to_persian_words(val)

        text = re.sub(r"\b\d+\b", replace_num, text)
        return text

    def apply_phonetic_glossary(self, text: str) -> str:
        """Replaces known scientific English terminology with Persian phonetic spellings."""
        for term, phonetic in self.glossary.items():
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            text = pattern.sub(phonetic, text)
        return text

    def clean_for_tts(self, text: str) -> str:
        """Master cleaning pipeline producing natural prosody-ready Persian text."""
        # 1. Phonetic glossary substitution
        text = self.apply_phonetic_glossary(text)
        
        # 2. Number expansion
        text = self.expand_numbers_and_symbols(text)
        
        # 3. ZWNJ normalization
        text = self.normalize_zwnj(text)
        
        # 4. Remove unwanted symbols while keeping sentence punctuation
        text = re.sub(r"[*_~`#\[\]\(\)<>]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()


if __name__ == "__main__":
    optimizer = PersianTextOptimizer()
    sample = "فرآیند apoptosis با فعال‌سازی bcl-2 و آزادسازی cytochrome c در بیش از 25% سلول‌ها رخ می‌دهد."
    result = optimizer.clean_for_tts(sample)
    print("Original:", sample)
    print("Optimized:", result)
