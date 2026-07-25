"""
Thanglish language module for CAELIS.
Provides vocabulary definitions, phrase sets, and helper functions
for recognizing and handling Tamil written in English script (Thanglish).
"""

import re

# Comprehensive list of common Thanglish words and keywords including STT phonetic variations
THANGLISH_VOCABULARY = {
    # Greetings & Salutations
    "vanakkam",
    "vanakam",
    "epdi",
    "empadi",
    "eppadi",
    "epdee",
    "iruka",
    "irukae",
    "irukiya",
    "irukeenga",
    "irukinga",
    "irukku",
    "iruku",
    # Questions & Pronouns
    "enna",
    "enanga",
    "yaru",
    "yaaru",
    "yen",
    "yeno",
    "edhuku",
    "eduku",
    "epo",
    "eppodhu",
    "enge",
    "yengae",
    "yenga",
    "un",
    "unnala",
    "nuna",
    "lana",
    "unga",
    "ungaloada",
    "nee",
    "neenga",
    "naan",
    "nanga",
    "nama",
    "nammalukku",
    # Common Verbs & Actions
    "pannu",
    "panra",
    "panren",
    "pannren",
    "pannunga",
    "pannanum",
    "panna",
    "mudiyum",
    "mudiyadhu",
    "sollu",
    "solla",
    "solldra",
    "solllu",
    "solllunga",
    "solunga",
    "pesu",
    "pesunga",
    "kelu",
    "kaelu",
    "kelunga",
    "paru",
    "paaru",
    "parunga",
    "vaanga",
    "vanga",
    "ponga",
    "podu",
    "kudungaa",
    "kudu",
    "katungaa",
    "kaatunga",
    # Affirmations & Status
    "nalla",
    "nallaa",
    "super",
    "seri",
    "sari",
    "aama",
    "aamaa",
    "illa",
    "illai",
    "illapa",
    "venum",
    "vendam",
    "thavai",
    "saptiya",
    "sapta",
    "saapta",
    "purinjidhi",
    "purinjudhu",
    "puriyula",
    "puriyala",
    "teriyuma",
    "theriyuma",
    "teriyadhu",
    # Time & Date concepts
    "inniku",
    "innikku",
    "naalaikku",
    "naalaiki",
    "ippo",
    "ippoe",
    "mani",
    "neram",
    "velai",
    # Terms of address
    "machan",
    "machi",
    "thala",
    "thalai",
    "bro",
}

THANGLISH_PHRASES = [
    "epdi iruka",
    "empadi iruka",
    "epdi irukinga",
    "eppadi irukeenga",
    "nalla irukiya",
    "nalla iruken",
    "enna panra",
    "enna panren",
    "enna help venum",
    "unnala enna panna mudiyum",
    "nuna lana panra mudiyum",
    "un per enna",
    "un peyer enna",
    "yaaru nee",
    "nee yaaru",
    "inniku enna date",
    "ippo time enna",
    "mani enna",
    "enna time",
    "poitu varan",
    "open pannu",
    "close pannu",
    "stop pannu",
]


def is_thanglish_word(word: str) -> bool:
    return word.lower().strip() in THANGLISH_VOCABULARY


def score_thanglish(text: str) -> float:
    clean_text = text.lower().strip()
    if not clean_text:
        return 0.0

    for phrase in THANGLISH_PHRASES:
        if phrase in clean_text:
            return 0.9

    words = re.findall(r"\b\w+\b", clean_text)
    if not words:
        return 0.0

    matched = sum(1 for word in words if word in THANGLISH_VOCABULARY)
    return matched / len(words)
