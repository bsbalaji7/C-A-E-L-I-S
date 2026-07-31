import json
from pathlib import Path


DATA_DIR = Path("data/nlp")


def load_dataset():
    samples = []

    for file_name in ("english.json", "thanglish.json"):
        path = DATA_DIR / file_name

        if not path.exists():
            continue

        with open(path, "r", encoding="utf-8") as f:
            samples.extend(json.load(f))

    return samples