import re

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from caelis.language.transliterator import tamil_to_thanglish


tests = [
    "ஒன்னால என்ன பண்ண முடியும்",
    "என்ன பண்ற",
    "இப்போ மணி என்ன",
    "எப்படி இருக்க",
]


for text in tests:
    result = tamil_to_thanglish(text)

    print("Tamil :", text)
    print("Roman :", result)
    print("-" * 40)

TAMIL_PATTERN = re.compile(r"[\u0B80-\u0BFF]")


# CAELIS-specific normalization.
# Library transliteration gives us a consistent Roman representation;
# these replacements make common spoken Tamil closer to natural Thanglish.
WORD_NORMALIZATIONS = {
    "eṉṉa": "enna",
    "eṉṉāl": "ennal",
    "uṉṉāl": "unnala",
    "oṉṉāl": "unnala",
    "nī": "nee",
    "nāṉ": "naan",
    "nalla": "nalla",
    "eppaṭi": "epdi",
    "irukka": "iruka",
    "irukkiṟāy": "iruka",
    "paṇṇa": "panna",
    "paṇṇu": "pannu",
    "muṭiyum": "mudiyum",
    "collu": "sollu",
    "cella": "sella",
    "nēram": "neram",
    "maṇi": "mani",
    "iṉṉaikku": "inniku",
    "ippōtu": "ippo",
}

tests = [
    "ஒன்னால என்ன பண்ண முடியும்",
    "என்ன பண்ற",
    "இப்போ மணி என்ன",
    "எப்படி இருக்க",
]


for text in tests:
    result = tamil_to_thanglish(text)

    print("Tamil :", text)
    print("Roman :", result)
    print("-" * 40)

def contains_tamil(text: str) -> bool:
    if not text:
        return False

    return bool(TAMIL_PATTERN.search(text))


def tamil_to_thanglish(text: str) -> str:
    """
    Convert Tamil Unicode text into Romanized text suitable
    for CAELIS language detection and intent processing.

    Example target:
        ஒன்னால என்ன பண்ண முடியும்
            ->
        unnala enna panna mudiyum
    """

    if not text:
        return ""

    text = str(text).strip()

    if not contains_tamil(text):
        return text

    try:
        # ITRANS produces Roman-script transliteration.
        romanized = transliterate(
            text,
            sanscript.TAMIL,
            sanscript.ITRANS,
        )

    except Exception as error:
        print(f"[TRANSLITERATOR ERROR] {error}")
        return text

    romanized = romanized.lower()

    # Apply known spoken-Tamil normalizations.
    for source, target in WORD_NORMALIZATIONS.items():
        romanized = romanized.replace(
            source.lower(),
            target,
        )

    # Remove transliteration punctuation/markers that are
    # unnecessary for CAELIS intent matching.
    romanized = re.sub(
        r"[^a-zA-Z0-9\s'-]",
        "",
        romanized,
    )

    romanized = re.sub(
        r"\s+",
        " ",
        romanized,
    ).strip()

    return romanized


def normalize_voice_text(text: str) -> tuple[str, str]:
    """
    Normalize STT output before sending it to CAELIS Brain.

    Returns:
        (normalized_text, language)

    Tamil-script Whisper output is converted to Romanized
    Thanglish and marked as Thanglish.
    """

    if not text:
        return "", "english"

    text = str(text).strip()

    if contains_tamil(text):
        converted = tamil_to_thanglish(text)

        print(f"[LANG] Tamil STT: {text}")
        print(f"[LANG] Romanized: {converted}")

        return converted, "thanglish"

    # Import here to avoid unnecessary circular imports.
    from caelis.language.detector import detect_language

    return text, detect_language(text)