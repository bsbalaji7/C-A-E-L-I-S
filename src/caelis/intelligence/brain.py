import re
from datetime import datetime

from caelis.intelligence.local_ai import LocalAI
from caelis.intelligence.personality import (
    get_greeting,
    NAME,
    FULL_NAME,
    USER_NAME,
)


class Brain:
    """
    CAELIS intelligence layer.

    Common commands are processed locally for maximum speed.
    Open-ended conversation falls back to the local Ollama AI.
    """

    def __init__(self):
        print("[BRAIN] Initializing intelligence...")

        self.local_ai = LocalAI()

        print("[BRAIN] Local AI ready.")

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
                return f"Enakku onnum kekala {USER_NAME}."

            return f"I didn't hear anything, {USER_NAME}."

        # Normalize incoming STT text.
        raw_clean = self._normalize(text)
        tokens = set(raw_clean.split())

        print(f"[BRAIN] Normalized: {raw_clean}")
        print(f"[BRAIN] Language: {language}")

        # =====================================================
        # 1. STATUS / HOW ARE YOU
        # =====================================================

        status_phrases = {
            "how are you",
            "how are you doing",
            "hows it going",
            "how you doing",

            "epdi iruka",
            "epdi irukeenga",
            "epdi irukinga",

            "eppadi iruka",
            "eppadi irukeenga",
            "eppadi irukinga",

            "empadi iruka",
            "empadi irukeenga",

            "nalla irukiya",
            "nalla irukingala",
        }

        is_status = (
            raw_clean in status_phrases

            or any(
                phrase in raw_clean
                for phrase in [
                    "how are you",
                    "hows it going",
                    "epdi iruk",
                    "eppadi iruk",
                    "empadi iruk",
                    "nalla iruk",
                ]
            )
        )

        if is_status:
            print("[BRAIN] Local intent: STATUS")

            if language in ("thanglish", "tamil"):
                return (
                    f"Naan super-ah iruken {USER_NAME}! "
                    "Neenga epdi irukeenga?"
                )

            return (
                f"I'm doing great, {USER_NAME}! "
                "How are you doing?"
            )

        # =====================================================
        # 2. GREETING
        # =====================================================

        greeting_phrases = {
            "hi",
            "hii",
            "hello",
            "hey",

            "hi caelis",
            "hello caelis",
            "hey caelis",

            "hi bro",
            "hey bro",
            "hi machan",
            "hey machan",

            "vanakkam",
            "vanakam",

            "good morning",
            "good afternoon",
            "good evening",
        }

        is_greeting = (
            raw_clean in greeting_phrases

            or any(
                phrase in raw_clean
                for phrase in [
                    "vanakkam",
                    "vanakam",
                    "hello caelis",
                    "hey caelis",
                    "hi caelis",
                ]
            )
        )

        if is_greeting:
            print("[BRAIN] Local intent: GREETING")

            return self._greeting(language)

        # =====================================================
        # 3. IDENTITY
        # =====================================================

        identity_phrases = {
            "who are you",
            "what are you",

            "what is your name",
            "whats your name",
            "tell me your name",

            "who is caelis",

            "yaaru nee",
            "nee yaaru",

            "un per enna",
            "un peru enna",
            "un peyar enna",
            "un peyer enna",

            "caelis yaaru",
        }

        is_identity = (
            raw_clean in identity_phrases

            or any(
                phrase in raw_clean
                for phrase in [
                    "who are you",
                    "what is your name",
                    "whats your name",
                    "who is caelis",
                    "yaaru nee",
                    "nee yaaru",
                    "un per",
                    "un peru",
                    "un peyar",
                    "un peyer",
                    "caelis yaaru",
                ]
            )

            or (
                "yaaru" in tokens
                and "nee" in tokens
            )
        )

        if is_identity:
            print("[BRAIN] Local intent: IDENTITY")

            if language in ("thanglish", "tamil"):
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
        # 4. CAPABILITIES / HELP
        # =====================================================

        capability_phrases = {
            "what can you do",
            "what are your capabilities",
            "tell me what you can do",
            "how can you help me",
            "help me",

            "unnala enna panna mudiyum",
            "unnala enna panra mudiyum",
            "enna panna mudiyum",
            "enna panra mudiyum",

            "help pannu",
            "enna help panna mudiyum",
        }

        is_capabilities = (
            raw_clean in capability_phrases

            or any(
                phrase in raw_clean
                for phrase in [
                    "what can you do",
                    "your capabilities",
                    "panna mudiyum",
                    "panra mudiyum",
                    "help pannu",
                ]
            )

            or (
                "mudiyum" in tokens
                and bool(
                    tokens.intersection(
                        {
                            "panna",
                            "panra",
                            "unnala",
                            "enna",
                        }
                    )
                )
            )
        )

        if is_capabilities:
            print("[BRAIN] Local intent: CAPABILITIES")

            if language in ("thanglish", "tamil"):
                return (
                    f"{USER_NAME}, enakku neraya "
                    "visayam panna mudiyum. "
                    "Questions-ku answer pannuven, "
                    "information explain pannuven, "
                    "English-um Thanglish-um pesuven, "
                    "and supported system tasks-um "
                    "handle pannuven."
                )

            return (
                f"{USER_NAME}, I can answer questions, "
                "explain concepts, have conversations, "
                "understand English and Thanglish, "
                "and handle supported system tasks."
            )

        # =====================================================
        # 5. TIME
        # =====================================================

        time_phrases = {
            "what time is it",
            "what is the time",
            "whats the time",

            "tell me the time",
            "tell the time",

            "current time",
            "time now",

            "ippo time enna",
            "ippo enna time",

            "mani enna",
            "enna mani",

            "enna time",
            "time enna",
        }

        is_time = (
            raw_clean in time_phrases

            or (
                "time" in tokens
                and bool(
                    tokens.intersection(
                        {
                            "what",
                            "current",
                            "now",
                            "enna",
                            "ippo",
                        }
                    )
                )
            )

            or (
                "mani" in tokens
                and "enna" in tokens
            )
        )

        if is_time:
            print("[BRAIN] Local intent: TIME")

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            if language in ("thanglish", "tamil"):
                return (
                    f"{USER_NAME}, ippo time "
                    f"{current_time}."
                )

            return (
                f"The current time is "
                f"{current_time}."
            )

        # =====================================================
        # 6. DATE
        # =====================================================

        date_phrases = {
            "what is the date",
            "what date is it",
            "whats the date",

            "tell me the date",

            "todays date",
            "today date",
            "current date",

            "inniku date enna",
            "inniku enna date",

            "date enna",
            "enna date",
        }

        is_date = (
            raw_clean in date_phrases

            or (
                "date" in tokens
                and bool(
                    tokens.intersection(
                        {
                            "what",
                            "today",
                            "current",
                            "enna",
                            "inniku",
                        }
                    )
                )
            )
        )

        if is_date:
            print("[BRAIN] Local intent: DATE")

            current_date = datetime.now().strftime(
                "%A, %d %B %Y"
            )

            if language in ("thanglish", "tamil"):
                return (
                    f"{USER_NAME}, inniku date "
                    f"{current_date}."
                )

            return (
                f"Today is {current_date}."
            )

        # =====================================================
        # 7. GENERAL CONVERSATION -> OLLAMA
        # =====================================================

        print(
            "[BRAIN] No local intent matched."
        )

        print(
            "[BRAIN] Sending conversation to local AI "
            f"(language={language})..."
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
                f"[BRAIN ERROR] {error}"
            )

        # =====================================================
        # 8. AI FAILURE FALLBACK
        # =====================================================

        if language in ("thanglish", "tamil"):
            return (
                f"{USER_NAME}, ennoda local AI "
                "ippo respond pannala. "
                "Konjam neram kalichu try pannunga."
            )

        return (
            f"My local AI isn't responding right now, "
            f"{USER_NAME}. Please try again."
        )

    # =========================================================
    # NORMALIZER
    # =========================================================

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize STT/user text before intent detection.

        Example:
            "What is the time?"
                    ->
            "what is the time"
        """

        text = text.lower().strip()

        # Replace punctuation with spaces instead of simply
        # deleting it, so words don't accidentally join.
        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
            flags=re.UNICODE,
        )

        # Collapse repeated spaces.
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # =========================================================
    # GREETING
    # =========================================================

    @staticmethod
    def _greeting(language: str) -> str:
        return get_greeting(language)