import re
import ollama


class LocalAI:
    def __init__(self):
        self.model = "llama3:instruct"
        self.history = []

    def generate(
        self,
        message: str,
        language: str = "english",
    ) -> str:

        system_prompt = f"""
You are CAELIS, a Cognitive Autonomous Entity with Lucidity, Intelligence and Synthesis.
You are BS's personal AI voice assistant.

CRITICAL VOICE INSTRUCTIONS:
1. Keep answers strictly 1 to 2 short sentences.
2. NEVER use brackets, markdown, bullet points, numbers, or tags like [Nalla].
3. Speak directly as CAELIS.

LANGUAGE & SCRIPT INSTRUCTIONS:
1. Active detected language: {language.upper()}
2. If the user speaks English, respond in clear, natural English.
3. If the user speaks Thanglish or Tamil, ALWAYS reply in natural Thanglish using English/Latin alphabet.

EXAMPLES:
User: "Epdi iruka?"
CAELIS: "Nalla iruken BS. Neenga epdi irukeenga?"

User: "Enna panra?"
CAELIS: "Ungalukku help panna ready-ah iruken BS."

User: "What can you do?"
CAELIS: "I can assist you with answering questions and managing your tasks in both English and Thanglish."
""".strip()

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(self.history[-6:])

        messages.append(
            {
                "role": "user",
                "content": f"[{language.upper()}] {message}",
            }
        )

        print(f"[OLLAMA] Model: {self.model} | Lang: {language}")

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "num_predict": 50,  # Fast generation limit for short voice output
                "temperature": 0.5,
            },
        )

        answer = response["message"]["content"].strip()
        answer = self._clean_speech_text(answer)

        self.history.append(
            {
                "role": "user",
                "content": message,
            }
        )

        self.history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return answer

    @staticmethod
    def _clean_speech_text(text: str) -> str:
        """Removes markdown symbols, square brackets, and tags for clean speech."""
        # Strip square brackets and text inside brackets like [Nalla]
        text = re.sub(r"\[.*?\]", "", text)
        # Strip markdown symbols
        text = re.sub(r"[\*\#\`\~\_\-\>]", "", text)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)
        return text.strip()