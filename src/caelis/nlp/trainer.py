from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from caelis.nlp.dataset import load_dataset


MODEL_DIR = Path("models/nlp")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def train():

    data = load_dataset()

    texts = [d["text"] for d in data]
    labels = [d["intent"] for d in data]

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(2, 5)
            ),
        ),
        (
            "classifier",
            LinearSVC()
        )
    ])

    model.fit(texts, labels)

    joblib.dump(
        model,
        MODEL_DIR / "intent_model.joblib"
    )

    print("Training Complete")
    print(f"Samples : {len(texts)}")


if __name__ == "__main__":
    train()