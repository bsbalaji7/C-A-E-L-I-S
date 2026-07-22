import re


TAMIL_PATTERN = re.compile(r"[\u0B80-\u0BFF]")

THANGLISH_WORDS = {
    "enna",
    "epdi",
    "eppadi",
    "iruka",
    "irukku",
    "pannu",
    "panra",
    "panren",
    "venum",
    "illa",
    "seri",
    "sari",
    " sollu",
    "open pannu",
}


def detect_language(text: str) -> str:
    text = text.strip().lower()

    if TAMIL_PATTERN.search(text):
        return "tamil"

    if any(word.strip() in text for word in THANGLISH_WORDS):
        return "thanglish"

    return "english"