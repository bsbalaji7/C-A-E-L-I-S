from datetime import datetime


class Brain:
    def process(self, text: str, language: str) -> str:
        command = text.lower().strip()

        if command in {"hi", "hello", "hey", "hii"}:
            return self._greeting(language)

        if "your name" in command or "who are you" in command:
            return (
                "I am CAELIS — Cognitive Autonomous Entity "
                "with Lucidity, Intelligence & Synthesis."
            )

        if "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."

        if language == "tamil":
            return "நான் புரிந்துகொண்டேன். ஆனால் அந்த திறன் இன்னும் உருவாக்கப்பட்டு வருகிறது."

        if language == "thanglish":
            return "Purinjithu BS. Aana indha feature innum build pannitu irukkom."

        return (
            "I understand your request, but that capability "
            "hasn't been implemented yet."
        )

    @staticmethod
    def _greeting(language: str) -> str:
        if language == "tamil":
            return "வணக்கம் BS. நான் CAELIS. எப்படி உதவலாம்?"

        if language == "thanglish":
            return "Vanakkam BS. Naan CAELIS. Enna help venum?"

        return "Hello BS. I'm CAELIS. How can I assist you?"