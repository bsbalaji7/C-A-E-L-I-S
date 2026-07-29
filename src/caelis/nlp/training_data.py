INTENTS = {
    # =====================================================
    # GREETING
    # =====================================================
    "greeting": {
        "patterns": [
            "hi",
            "hello",
            "hey",
            "hello caelis",
            "hi caelis",
            "hey caelis",

            "vanakkam",
            "vanakam",

            "hi bro",
            "hello bro",
            "hi machan",

            "good morning",
            "good afternoon",
            "good evening",
        ],

        "responses": {
            "english": [
                "Hello BS. How can I help you?"
            ],

            "thanglish": [
                "Vanakkam BS. Enna help venum?"
            ],
        },
    },

    # =====================================================
    # STATUS
    # =====================================================
    "status": {
        "patterns": [
            "how are you",
            "how are you doing",
            "how you doing",
            "how is it going",

            "epdi iruka",
            "epdi irukeenga",
            "nalla iruka",
            "nalla irukiya",
        ],

        "responses": {
            "english": [
                "I'm doing great BS. How are you?"
            ],

            "thanglish": [
                "Naan super ah iruken BS. Neenga epdi irukeenga?"
            ],
        },
    },

    # =====================================================
    # IDENTITY
    # =====================================================
    "identity": {
        "patterns": [
            "who are you",
            "what is your name",
            "tell me your name",
            "who is caelis",

            "nee yaaru",
            "yaaru nee",
            "un peru enna",
            "caelis yaaru",
        ],

        "responses": {
            "english": [
                "I am CAELIS, your personal AI assistant."
            ],

            "thanglish": [
                "Naan CAELIS BS. Unga personal AI assistant."
            ],
        },
    },

    # =====================================================
    # CAPABILITIES
    # =====================================================
    "capabilities": {
        "patterns": [
            "what can you do",
            "what are your capabilities",
            "how can you help me",
            "help me",

            "unnala enna panna mudiyum",
            "enna panna mudiyum",
            "enna help panna mudiyum",
            "help pannu",
        ],

        "responses": {
            "english": [
                "I can answer questions, understand commands, control supported applications, and assist you with tasks."
            ],

            "thanglish": [
                "BS, questions answer pannuven, commands understand pannuven, supported apps control pannuven, ungalukku tasks la help pannuven."
            ],
        },
    },

    # =====================================================
    # TIME
    # =====================================================
    "time": {
        "patterns": [
            "what time is it",
            "what is the time",
            "tell me the time",
            "current time",
            "time now",

            "ippo time enna",
            "ippo enna time",
            "time enna",
            "mani enna",
            "enna mani",
        ],
    },

    # =====================================================
    # DATE
    # =====================================================
    "date": {
        "patterns": [
            "what is the date",
            "what date is it",
            "tell me the date",
            "today date",
            "current date",

            "inniku date enna",
            "inniku enna date",
            "date enna",
            "enna date",
        ],
    },

    # =====================================================
    # OPEN APPLICATION
    # =====================================================
    "open_app": {
        "patterns": [
            "open chrome",
            "open google chrome",
            "chrome open pannu",

            "open notepad",
            "notepad open pannu",

            "open calculator",
            "calculator open pannu",

            "open vscode",
            "open vs code",
            "vs code open pannu",

            "open file explorer",
            "file explorer open pannu",
        ],
    },

    # =====================================================
    # CLOSE APPLICATION
    # =====================================================
    "close_app": {
        "patterns": [
            "close chrome",
            "chrome close pannu",

            "close notepad",
            "notepad close pannu",

            "close calculator",
            "calculator close pannu",

            "close vscode",
            "vs code close pannu",
        ],
    },

    # =====================================================
    # THANKS
    # =====================================================
    "thanks": {
        "patterns": [
            "thanks",
            "thank you",
            "thank you caelis",

            "nandri",
            "romba nandri",
            "thanks macha",
        ],

        "responses": {
            "english": [
                "You're welcome BS."
            ],

            "thanglish": [
                "Anytime BS."
            ],
        },
    },
}