from datetime import datetime
import random

from caelis.intelligence.personality import (
    NAME,
    FULL_NAME,
    USER_NAME,
)

from caelis.nlp.classifier import IntentClassifier
from caelis.nlp.entities import extract_entities
from caelis.nlp.training_data import INTENTS


class Brain:
    """
    CAELIS Brain

    Fully local intelligence layer.

    Pipeline:

        Speech/Text
             ↓
        Intent Classifier
             ↓
        Entity Extractor
             ↓
        Brain
             ↓
        Response / System Task

    No Ollama.
    No external APIs.
    """

    def __init__(self):

        print("[BRAIN] Initializing...")

        self.classifier = IntentClassifier()

        print("[BRAIN] Local ML ready.")

    # =====================================================
    # MAIN PROCESSOR
    # =====================================================

    def process(
        self,
        text: str,
        language: str = "english",
    ) -> str:

        if not text or not text.strip():

            if self._is_thanglish(language):
                return (
                    f"Enakku onnum kekala "
                    f"{USER_NAME}."
                )

            return (
                f"I didn't hear anything, "
                f"{USER_NAME}."
            )

        print()
        print("=" * 60)
        print("[BRAIN]")
        print(f"Input      : {text}")
        print(f"Language   : {language}")

        # -----------------------------
        # Intent Prediction
        # -----------------------------

        intent = self.classifier.predict(text)

        print(f"Intent     : {intent}")

        # -----------------------------
        # Entity Extraction
        # -----------------------------

        entities = extract_entities(text)

        print(f"Entities   : {entities}")

        # =================================================
        # GREETING
        # =================================================

        if intent == "greeting":

            return self._intent_response(
                "greeting",
                language,
            )

        # =================================================
        # STATUS
        # =================================================

        if intent == "status":

            return self._intent_response(
                "status",
                language,
            )

        # =================================================
        # IDENTITY
        # =================================================

        if intent == "identity":

            if self._is_thanglish(language):

                return (
                    f"Naan {NAME}, "
                    f"{FULL_NAME}. "
                    f"Naan unga personal "
                    f"AI assistant "
                    f"{USER_NAME}."
                )

            return (
                f"I am {NAME}, "
                f"{FULL_NAME}. "
                f"I'm your personal "
                f"AI assistant, "
                f"{USER_NAME}."
            )

        # =================================================
        # CAPABILITIES
        # =================================================

        if intent == "capabilities":

            return self._intent_response(
                "capabilities",
                language,
            )

        # =================================================
        # TIME
        # =================================================

        if intent == "time":

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            if self._is_thanglish(language):

                return (
                    f"{USER_NAME}, "
                    f"ippo time "
                    f"{current_time}."
                )

            return (
                f"The current time is "
                f"{current_time}."
            ) 
                # =================================================
        # DATE
        # =================================================

        if intent == "date":

            current_date = datetime.now().strftime("%d %B %Y")

            if self._is_thanglish(language):
                return f"{USER_NAME}, inniku date {current_date}."

            return f"Today's date is {current_date}."

        # =================================================
        # THANKS
        # =================================================

        if intent == "thanks":
            return self._intent_response(
                "thanks",
                language,
            )

        # =================================================
        # OPEN APP
        # =================================================

        if intent == "open_app":

            app = entities.get("application")

            if app:

                if self._is_thanglish(language):
                    return f"Sari {USER_NAME}, {app} open panren."

                return f"Opening {app}."

            if self._is_thanglish(language):
                return "Yentha application open pannanum?"

            return "Which application would you like me to open?"

        # =================================================
        # CLOSE APP
        # =================================================

        if intent == "close_app":

            app = entities.get("application")

            if app:

                if self._is_thanglish(language):
                    return f"Sari {USER_NAME}, {app} close panren."

                return f"Closing {app}."

            if self._is_thanglish(language):
                return "Yentha application close pannanum?"

            return "Which application would you like me to close?"

        # =================================================
        # EXIT
        # =================================================

        if intent == "exit":

            if self._is_thanglish(language):
                return f"Bye {USER_NAME}. Naan eppovum ready."

            return f"Goodbye {USER_NAME}. Have a great day."

        # =================================================
        # FALLBACK
        # =================================================

        if self._is_thanglish(language):
            return (
                "Adha purinjika mudiyala. "
                "Konjam vera madhiri sollunga."
            )

        return (
            "Sorry, I couldn't understand that."
        )

    # =====================================================
    # HELPERS
    # =====================================================

    def _is_thanglish(self, language: str) -> bool:
        return language.lower() in (
            "thanglish",
            "tamil",
        )

    def _intent_response(
        self,
        intent: str,
        language: str,
    ) -> str:

        responses = INTENTS.get(intent, {}).get(
            "responses",
            {}
        )

        if self._is_thanglish(language):

            choices = responses.get(
                "thanglish",
                []
            )

            if choices:
                return random.choice(choices)

        choices = responses.get(
            "english",
            []
        )

        if choices:
            return random.choice(choices)

        return "..."