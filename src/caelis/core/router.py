from caelis.intelligence.brain import Brain
from caelis.language.detector import detect_language


class Router:
    def __init__(self):
        self.brain = Brain()

    def route(self, user_input: str) -> str:
        language = detect_language(user_input)

        return self.brain.process(
            text=user_input,
            language=language,
        )