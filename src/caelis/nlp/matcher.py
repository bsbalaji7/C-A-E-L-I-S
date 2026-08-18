from difflib import SequenceMatcher

from caelis.nlp.intent import IntentResult
from caelis.nlp.normalizer import normalize_text
from caelis.nlp.training_data import INTENTS
from caelis.nlp.entities import extract_app


class IntentMatcher:
    def __init__(
        self,
        fuzzy_threshold: float = 0.78,
    ):
        self.fuzzy_threshold = fuzzy_threshold

    def match(self, text: str) -> IntentResult:
        normalized = normalize_text(text)

        if not normalized:
            return IntentResult(
                name="unknown",
                confidence=0.0,
            )

        # ---------------------------------------------
        # Exact match
        # ---------------------------------------------

        for intent_name, data in INTENTS.items():

            for pattern in data.get(
                "patterns",
                [],
            ):
                normalized_pattern = normalize_text(
                    pattern
                )

                if normalized == normalized_pattern:

                    entities = self._extract_entities(
                        intent_name,
                        normalized,
                    )

                    return IntentResult(
                        name=intent_name,
                        confidence=1.0,
                        matched_pattern=pattern,
                        entities=entities,
                    )

        # ---------------------------------------------
        # Fuzzy matching
        # ---------------------------------------------

        best_intent = "unknown"
        best_pattern = ""
        best_score = 0.0

        for intent_name, data in INTENTS.items():

            for pattern in data.get(
                "patterns",
                [],
            ):
                normalized_pattern = normalize_text(
                    pattern
                )

                score = SequenceMatcher(
                    None,
                    normalized,
                    normalized_pattern,
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_intent = intent_name
                    best_pattern = pattern

        if best_score >= self.fuzzy_threshold:

            entities = self._extract_entities(
                best_intent,
                normalized,
            )

            return IntentResult(
                name=best_intent,
                confidence=best_score,
                matched_pattern=best_pattern,
                entities=entities,
            )

        return IntentResult(
            name="unknown",
            confidence=best_score,
            matched_pattern=best_pattern,
        )

    @staticmethod
    def _extract_entities(
        intent_name: str,
        text: str,
    ) -> dict:

        entities = {}

        if intent_name in {
            "open_app",
            "close_app",
        }:
            app = extract_app(text)

            if app:
                entities["app"] = app

        return entities