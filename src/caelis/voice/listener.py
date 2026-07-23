import speech_recognition as sr


class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self) -> str | None:
        with sr.Microphone() as source:
            print("Listening...")

            try:
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5,
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10,
                )

            except sr.WaitTimeoutError:
                return None

        try:
            # English recognition works reasonably well for
            # English and many Thanglish phrases.
            text = self.recognizer.recognize_google(
                audio,
                language="en-IN",
            )

            print(f"BS: {text}")

            return text

        except sr.UnknownValueError:
            print("CAELIS: Speech not understood.")
            return None

        except sr.RequestError as error:
            print(f"Speech recognition error: {error}")
            return None