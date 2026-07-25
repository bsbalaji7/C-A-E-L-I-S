"""
Language detector for CAELIS.
Detects whether input text is in Tamil script, Thanglish, or English.
"""

import re
from caelis.language.thanglish import score_thanglish, THANGLISH_VOCABULARY

TAMIL_PATTERN = re.compile(r"[\u0B80-\u0BFF]")


def detect_language(text: str) -> str:
    """
    Detect language of the input text.

    Returns:
        "tamil"     if script contains Tamil Unicode characters
        "thanglish" if text contains Thanglish vocabulary or patterns
        "english"   default fallback
    """
    if not text:
        return "english"

    cleaned = text.strip().lower()

    # 1. Tamil script check
    if TAMIL_PATTERN.search(cleaned):
        return "tamil"

    # 2. Thanglish scoring check
    score = score_thanglish(cleaned)
    if score >= 0.25:
        return "thanglish"

    # 3. Check for any explicit Thanglish word boundary match
    words = set(re.findall(r"\b\w+\b", cleaned))
    if words.intersection(THANGLISH_VOCABULARY):
        return "thanglish"

    return "english"