from caelis.nlp import IntentMatcher


nlp = IntentMatcher()


tests = [
    "What is the time?",
    "What time is it?",
    "Ippo time enna?",
    "What is the date?",
    "Inn iku date enna?",
    "How are you?",
    "Eppadi irukka?",
    "Unnala enna panna mudiyum?",
    "Chrome open pannu",
    "Open calculator",
    "Vanakkam",
    "Who are you?",
]


for text in tests:
    result = nlp.match(text)

    print()
    print("=" * 60)
    print(f"INPUT      : {text}")
    print(f"INTENT     : {result.name}")
    print(f"CONFIDENCE : {result.confidence:.2f}")
    print(f"PATTERN    : {result.matched_pattern}")
    print(f"ENTITIES   : {result.entities}")