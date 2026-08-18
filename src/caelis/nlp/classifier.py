from pathlib import Path
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class IntentClassifier:
    """
    Local ML Intent Classifier

    Uses:
        TF-IDF
        +
        Logistic Regression
    """

    def __init__(self):

        model_dir = Path("models/nlp")

        self.vectorizer_path = model_dir / "vectorizer.pkl"
        self.model_path = model_dir / "intent_model.pkl"

        self.vectorizer = None
        self.model = None

        self._load()

    # --------------------------------------------------

    def _load(self):

        if not self.vectorizer_path.exists():
            raise FileNotFoundError(
                "vectorizer.pkl not found.\n"
                "Run:\n"
                "python -m caelis.nlp.trainer"
            )

        if not self.model_path.exists():
            raise FileNotFoundError(
                "intent_model.pkl not found.\n"
                "Run:\n"
                "python -m caelis.nlp.trainer"
            )

        with open(self.vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)

        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    # --------------------------------------------------

    def predict(self, text: str) -> str:

        if not text:
            return "unknown"

        text = text.strip()

        if not text:
            return "unknown"

        vector = self.vectorizer.transform([text])

        prediction = self.model.predict(vector)[0]

        return prediction

    # --------------------------------------------------

    def predict_proba(self, text: str):

        vector = self.vectorizer.transform([text])

        probabilities = self.model.predict_proba(vector)[0]

        labels = self.model.classes_

        return dict(zip(labels, probabilities))

    # --------------------------------------------------

    def confidence(self, text: str) -> float:

        probs = self.predict_proba(text)

        return max(probs.values())