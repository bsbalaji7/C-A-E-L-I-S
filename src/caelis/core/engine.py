from caelis.core.router import Router
from caelis.voice.listener import VoiceListener
from caelis.voice.speech import Voice


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
        print("Language ........ ONLINE")
        print("Intelligence .... ONLINE")
        print("Voice ........... ONLINE")
        print("Memory .......... STANDBY")
        print("System .......... STANDBY")
        print()

        self.voice.speak(
            "CAELIS online. Hello BS. How can I assist you?"
        )

        self.run()

    def run(self):
        while self.running:
            try:
                user_input = self.listener.listen()

                if not user_input:
                    continue

                command = user_input.lower().strip()

                if command in {
                    "exit",
                    "quit",
                    "shutdown",
                    "goodbye",
                    "bye",
                }:
                    self.shutdown()
                    continue

                response = self.router.route(user_input)

                self.voice.speak(response)

            except KeyboardInterrupt:
                self.shutdown()

    def shutdown(self):
        self.voice.speak(
            "Shutting down. Goodbye BS."
        )

        self.running = False