from pathlib import Path

import joblib


MODEL = Path("models/nlp/intent_model.joblib")


class IntentClassifier:

    def __init__(self):

        if not MODEL.exists():
            raise FileNotFoundError(
                "Train the model first."
            )

        self.model = joblib.load(MODEL)

    def predict(self, text):

        intent = self.model.predict([text])[0]

        return intent