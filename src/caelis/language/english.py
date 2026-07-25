"""
English language module for CAELIS.
Provides vocabulary definitions, phrase sets, and helper functions
for recognizing standard English inputs.
"""

ENGLISH_GREETINGS = {
    "hi",
    "hello",
    "hey",
    "hii",
    "good morning",
    "good afternoon",
    "good evening",
    "hello caelis",
    "hey caelis",
    "hi caelis",
}

ENGLISH_IDENTITY = {
    "who are you",
    "what are you",
    "what is your name",
    "what's your name",
    "tell me your name",
    "who is caelis",
}

ENGLISH_TIME = {
    "what time is it",
    "what is the time",
    "tell me the time",
    "current time",
    "time now",
}

ENGLISH_DATE = {
    "what is the date",
    "what's the date",
    "today's date",
    "todays date",
    "current date",
}

ENGLISH_STATUS = {
    "how are you",
    "how's it going",
    "how are you doing",
    "how do you do",
}

ENGLISH_CAPABILITIES = {
    "what can you do",
    "what are your capabilities",
    "help me",
    "help",
    "what are your features",
}


def is_english_greeting(text: str) -> bool:
    return text.lower().strip() in ENGLISH_GREETINGS
