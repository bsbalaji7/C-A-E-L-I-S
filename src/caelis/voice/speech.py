import re
import pyttsx3
import threading


class Voice:
    def __init__(self):
        self.rate = 175
        self.volume = 1.0
        self.lock = threading.Lock()

        print("[VOICE] Speech system ready.")

    def _create_engine(self):
        engine = pyttsx3.init(driverName="sapi5")
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        return engine

    def _prepare_text_for_tts(self, text: str) -> str:
        """
        Preprocesses text so Thanglish and English sound natural
        when spoken aloud by the SAPI5 TTS engine.
        """
        text = str(text).strip()
        # Remove any bracketed tags like [Nalla]
        text = re.sub(r"\[.*?\]", "", text)
        # Remove markdown symbols
        text = re.sub(r"[\*\#\`\~\_\-\>]", "", text)
        # Ensure smooth pause formatting
        text = text.replace("...", ". ").replace("  ", " ")
        return text.strip()

    def speak(self, text: str):
        if not text:
            return

        clean_text = self._prepare_text_for_tts(text)
        if not clean_text:
            return

        print(f"CAELIS: {clean_text}")

        with self.lock:
            engine = None
            try:
                engine = self._create_engine()
                engine.say(clean_text)
                engine.runAndWait()

            except Exception as error:
                print(f"[TTS ERROR] {error}")

            finally:
                if engine is not None:
                    try:
                        engine.stop()
                    except Exception:
                        pass