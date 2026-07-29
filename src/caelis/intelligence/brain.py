from datetime import datetime
import random

from caelis.intelligence.local_ai import LocalAI
from caelis.intelligence.personality import (
    NAME,
    FULL_NAME,
    USER_NAME,
)

from caelis.nlp import IntentMatcher
from caelis.nlp.training_data import INTENTS


class Brain:
    """
    CAELIS intelligence layer.

    Processing priority:

    1. CAELIS native NLP
    2. Local deterministic commands
    3. System commands
    4. Ollama only for unknown/open-ended queries
    """

    def __init__(self):
        print("[BRAIN] Initializing intelligence...")

        # Native CAELIS NLP
        self.nlp = IntentMatcher(
            fuzzy_threshold=0.78
        )

        print("[BRAIN] Native NLP ready.")

        # Ollama remains fallback only.
        try:
            self.local_ai = LocalAI()
            print("[BRAIN] Local AI fallback ready.")

        except Exception as error:
            print(
                f"[BRAIN] Local AI unavailable: {error}"
            )

            self.local_ai = None

    # =========================================================
    # MAIN PROCESSOR
    # =========================================================

    def process(
        self,
        text: str,
        language: str = "english",
    ) -> str:

        if not text or not text.strip():

            if language in ("thanglish", "tamil"):
                return (
                    f"Enakku onnum kekala "
                    f"{USER_NAME}."
                )

            return (
                f"I didn't hear anything, "
                f"{USER_NAME}."
            )

        print("[BRAIN] Processing...")
        print(f"[BRAIN] Input: {text}")
        print(f"[BRAIN] Language: {language}")

        # -----------------------------------------------------
        # Native NLP intent detection
        # -----------------------------------------------------

        result = self.nlp.match(text)

        print(
            f"[NLP] Intent: {result.name}"
        )

        print(
            f"[NLP] Confidence: "
            f"{result.confidence:.2f}"
        )

        if result.matched_pattern:
            print(
                f"[NLP] Pattern: "
                f"{result.matched_pattern}"
            )

        if result.entities:
            print(
                f"[NLP] Entities: "
                f"{result.entities}"
            )

        # =====================================================
        # GREETING
        # =====================================================

        if result.name == "greeting":

            print(
                "[BRAIN] Local response: GREETING"
            )

            return self._intent_response(
                "greeting",
                language,
            )

        # =====================================================
        # STATUS
        # =====================================================

        if result.name == "status":

            print(
                "[BRAIN] Local response: STATUS"
            )

            return self._intent_response(
                "status",
                language,
            )

        # =====================================================
        # IDENTITY
        # =====================================================

        if result.name == "identity":

            print(
                "[BRAIN] Local response: IDENTITY"
            )

            if self._is_thanglish(language):

                return (
                    f"Naan {NAME}, {FULL_NAME}. "
                    f"Naan unga personal AI assistant "
                    f"{USER_NAME}."
                )

            return (
                f"I am {NAME}, {FULL_NAME}. "
                f"I'm your personal AI assistant, "
                f"{USER_NAME}."
            )

        # =====================================================
        # CAPABILITIES
        # =====================================================

        if result.name == "capabilities":

            print(
                "[BRAIN] Local response: CAPABILITIES"
            )

            return self._intent_response(
                "capabilities",
                language,
            )

        # =====================================================
        # TIME
        # =====================================================

        if result.name == "time":

            print(
                "[BRAIN] Local response: TIME"
            )

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            if self._is_thanglish(language):

                return (
                    f"{USER_NAME}, ippo time "
                    f"{current_time}."
                )

            return (
                f"The current time is "
                f"{current_time}."
            )

        # =====================================================
        # DATE
        # =====================================================

        if result.name == "date":

            print(
                "[BRAIN] Local response: DATE"
            )

            current_date = datetime.now().strftime(
                "%A, %d %B %Y"
            )

            if self._is_thanglish(language):

                return (
                    f"{USER_NAME}, inniku date "
                    f"{current_date}."
                )

            return (
                f"Today is {current_date}."
            )

        # =====================================================
        # THANKS
        # =====================================================

        if result.name == "thanks":

            print(
                "[BRAIN] Local response: THANKS"
            )

            return self._intent_response(
                "thanks",
                language,
            )

        # =====================================================
        # OPEN APPLICATION
        # =====================================================

        if result.name == "open_app":

            app = result.entities.get("app")

            print(
                f"[BRAIN] System intent: "
                f"OPEN_APP -> {app}"
            )

            if not app:

                if self._is_thanglish(language):
                    return (
                        f"{USER_NAME}, endha app "
                        "open pannanum?"
                    )

                return (
                    f"{USER_NAME}, which application "
                    "should I open?"
                )

            # Actual application execution will be
            # connected in the next development step.

            if self._is_thanglish(language):

                return (
                    f"Seri {USER_NAME}. "
                    f"{app} open panna ready."
                )

            return (
                f"Okay {USER_NAME}. "
                f"{app} is ready to be opened."
            )

        # =====================================================
        # CLOSE APPLICATION
        # =====================================================

        if result.name == "close_app":

            app = result.entities.get("app")

            print(
                f"[BRAIN] System intent: "
                f"CLOSE_APP -> {app}"
            )

            if not app:

                if self._is_thanglish(language):
                    return (
                        f"{USER_NAME}, endha app "
                        "close pannanum?"
                    )

                return (
                    f"{USER_NAME}, which application "
                    "should I close?"
                )

            if self._is_thanglish(language):

                return (
                    f"Seri {USER_NAME}. "
                    f"{app} close panna ready."
                )

            return (
                f"Okay {USER_NAME}. "
                f"{app} is ready to be closed."
            )

        # =====================================================
        # UNKNOWN
        # =====================================================

        print(
            "[BRAIN] Native NLP did not understand "
            "the request."
        )

        # =====================================================
        # OPTIONAL OLLAMA FALLBACK
        # =====================================================

        if self.local_ai is not None:

            print(
                "[BRAIN] Using Ollama fallback..."
            )

            try:

                response = self.local_ai.generate(
                    message=text,
                    language=language,
                )

                if response:
                    return response.strip()

            except Exception as error:

                print(
                    f"[BRAIN ERROR] "
                    f"Ollama fallback failed: "
                    f"{error}"
                )

        # =====================================================
        # FINAL LOCAL FALLBACK
        # =====================================================

        if self._is_thanglish(language):

            return (
                f"{USER_NAME}, indha command enakku "
                "innum learn aagala. "
                "Training data-la add pannalaam."
            )

        return (
            f"{USER_NAME}, I haven't learned that "
            "command yet. We can add it to my "
            "training data."
        )

    # =========================================================
    # TRAINING DATA RESPONSE
    # =========================================================

    @staticmethod
    def _intent_response(
        intent_name: str,
        language: str,
    ) -> str:

        intent_data = INTENTS.get(
            intent_name,
            {}
        )

        responses = intent_data.get(
            "responses",
            {}
        )

        # Tamil speech currently uses Romanized
        # Thanglish output because the installed
        # SAPI voice is English.
        response_language = (
            "thanglish"
            if language in ("thanglish", "tamil")
            else "english"
        )

        available = responses.get(
            response_language,
            []
        )

        if available:
            return random.choice(available)

        # English backup.
        available = responses.get(
            "english",
            []
        )

        if available:
            return random.choice(available)

        return (
            f"{USER_NAME}, I understood the "
            f"{intent_name} command."
        )

    # =========================================================
    # LANGUAGE HELPER
    # =========================================================

    @staticmethod
    def _is_thanglish(
        language: str,
    ) -> bool:

        return language in (
            "thanglish",
            "tamil",
        )