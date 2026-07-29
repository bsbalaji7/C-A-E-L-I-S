 ##  Version Update For C.A.E.L.I.S 



 ##  C.A.E.L.I.S - v0.3
 We'll build CAELIS v0.3 for your 8 GB/Ryzen 3 machine in small steps so we can measure speed and accuracy after each change.

v0.3 plan
🎙️ "CAELIS"
      ↓
    ACTIVE
      ↓
🎙️ Command
      ↓
Tamil / English / Thanglish normalization
      ↓
Intent Router
   ↙       ↘
COMMAND     CONVERSATION
   ↓             ↓
Windows       Hybrid AI
   ↓             ↓
   └──────┬──────┘
          ↓
       🔊 Voice
          ↓
       STANDBY

We'll implement it in this order:

Wake-word mode — stop continuous expensive transcription.
Fast command router — commands bypass Ollama.
Thanglish normalizer — handle variations like pannu/panu/panna.
Windows actions — Chrome, VS Code, Notepad, Calculator, etc.
Conversational AI — cloud-first with lightweight local fallback.
STT optimization — benchmark accuracy/latency specifically with your voice.
Streaming TTS later.

For now, don't delete Whisper or Ollama. We'll reuse pieces while restructuring.

The first change will be the wake-word system, but instead of using Whisper continuously to detect "CAELIS"—which would defeat the purpose—we'll use a lightweight wake-word detector and activate the heavier STT only after CAELIS wakes.


 ##  C.A.E.L.I.S - v0.5.0

v0.5.0 details

The major achievement in this version is that CAELIS can understand known commands without Ollama:

"What is the time?"
        ↓
TIME (1.00)

"Eppadi irukka?"
        ↓
STATUS (1.00)

"Unnala enna panna mudiyum?"
        ↓
CAPABILITIES (1.00)

"Chrome open pannu"
        ↓
OPEN_APP (1.00)
app = chrome

You also now have:

src/caelis/nlp/
├── __init__.py
├── normalizer.py
├── intent.py
├── matcher.py
├── entities.py
└── training_data.py

And your test run showed all the sample English/Thanglish intents matching correctly, including a fuzzy match at 0.97.

Next — CAELIS v0.6.0

This is the significant upgrade you're proposing:

Remove Ollama and train CAELIS locally.

We'll add:

data/nlp/
├── english.json
└── thanglish.json

models/nlp/
└── intent_model.joblib

src/caelis/nlp/
├── dataset.py
├── trainer.py
└── classifier.py

Then:

Our dataset
    ↓
TF-IDF / character n-grams
    ↓
Local classifier training
    ↓
intent_model.joblib
    ↓
CAELIS loads model
    ↓
"What can you do?"
    ↓
CAPABILITIES

No Ollama required for intent recognition.

One caveat: this makes CAELIS trained for the intents and knowledge/actions we give it, not a general-purpose LLM that can answer arbitrary questions. We can build broader local knowledge and conversational capabilities separately.

I'd also add a project version constant now:

# src/caelis/core/config.py

CAELIS_VERSION = "0.5.0"
CAELIS_CODENAME = "Native NLP"

and startup could show:

C.A.E.L.I.S. v0.5.0
Native NLP

Core ............ ONLINE
Language ........ ONLINE
NLP ............. ONLINE
Intelligence .... ONLINE
Voice ........... ONLINE
Memory .......... STANDBY
System .......... STANDBY