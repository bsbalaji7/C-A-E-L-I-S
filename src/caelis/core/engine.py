from caelis.core.router import Router
from caelis.voice.listener import VoiceListener
from caelis.voice.speech import Voice
from caelis.language.detector import detect_language


class CaelisEngine:

    def __init__(self):
        self.router = Router()
        self.listener = VoiceListener()
        self.voice = Voice()

        self.running = False

    def start(self):
        self.running = True

        print()
        print("C.A.E.L.I.S. initializing...")
        print()
        print("Core ............ ONLINE")
        print("Language ........ ONLINE (English & Thanglish)")
        print("Intelligence .... ONLINE")
        print("Voice ........... ONLINE")
        print("Memory .......... STANDBY")
        print("System .......... STANDBY")
        print()

        self.speak(
            "CAELIS online. Hello BS! Naan CAELIS. How can I assist you?"
        )

        self.run()

    def run(self):

        while self.running:

            try:
                print()
                print("[VOICE] Waiting for command...")

                user_input = self.listener.listen()

                if not user_input:
                    continue

                print(f"[INPUT] {user_input}")

                command = user_input.lower().strip()

                # Shutdown commands (English & Thanglish)
                shutdown_phrases = {
                    "exit",
                    "quit",
                    "shutdown",
                    "goodbye",
                    "bye",
                    "stop caelis",
                    "close caelis",
                    "kilambu",
                    "kelambu",
                    "poidu",
                    "poitu varan",
                    "poitu varren",
                }

                if command in shutdown_phrases:
                    self.shutdown(user_input)
                    break

                print("[BRAIN] Processing...")

                try:
                    response = self.router.route(user_input)

                except Exception as error:
                    print(f"[BRAIN ERROR] {error}")

                    lang = detect_language(user_input)
                    if lang in ("thanglish", "tamil"):
                        response = "Process panradhula chinna error vandhurukku BS."
                    else:
                        response = "I encountered an error while processing that request."

                if not response:
                    response = "I don't have a response for that yet."

                print(f"[RESPONSE] {response}")

                self.speak(response)

            except KeyboardInterrupt:
                self.shutdown("quit")
                break

            except Exception as error:
                print(f"[ENGINE ERROR] {error}")

                self.speak(
                    "Something went wrong while processing your request."
                )

    def speak(self, text):

        if not text:
            return

        print(f"[SPEAK] {text}")

        try:
            self.voice.speak(str(text))

        except Exception as error:
            print(f"[VOICE ERROR] {error}")

    def shutdown(self, last_input: str = "bye"):
        if not self.running:
            return

        lang = detect_language(last_input)
        if lang in ("thanglish", "tamil"):
            bye_msg = "Seri BS, naan poidren. Goodbye!"
        else:
            bye_msg = "Shutting down CAELIS. Goodbye BS!"

        self.speak(bye_msg)
        self.running = False