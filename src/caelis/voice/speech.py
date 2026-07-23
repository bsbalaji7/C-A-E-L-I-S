import pyttsx3


class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        self._select_voice()

    def _select_voice(self):
        voices = self.engine.getProperty("voices")

        if not voices:
            return

        # Use the first available Windows voice for now.
        self.engine.setProperty(
            "voice",
            voices[0].id,
        )

    def speak(self, text: str):
        print(f"CAELIS: {text}")

        self.engine.say(text)
        self.engine.runAndWait()