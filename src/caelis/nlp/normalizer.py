import re


WORD_REPLACEMENTS = {
    # Thanglish phonetic variations
    "eppadi": "epdi",
    "epadi": "epdi",
    "empadi": "epdi",

    "irukka": "iruka",
    "irukkaa": "iruka",
    "irukiya": "iruka",

    "pannunga": "pannu",
    "pannuga": "pannu",

    "innikku": "inniku",
    "innaiku": "inniku",

    "ipo": "ippo",
    "ippoo": "ippo",

    "yaru": "yaaru",

    # Common STT variations
    "whats": "what is",
    "hows": "how is",
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()

    # Punctuation -> spaces
    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
        flags=re.UNICODE,
    )

    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    normalized_words = []

    for word in words:
        replacement = WORD_REPLACEMENTS.get(
            word,
            word,
        )

        normalized_words.extend(
            replacement.split()
        )

    return " ".join(normalized_words)