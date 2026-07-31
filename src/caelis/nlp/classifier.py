from pathlib import Path
import joblib


MODEL_PATH = Path("models/nlp/intent_model.joblib")


class IntentClassifier:

    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Model not found. Run trainer first."
            )

        self.model = joblib.load(MODEL_PATH)

    def predict(self, text: str):
        return self.model.predict([text])[0]