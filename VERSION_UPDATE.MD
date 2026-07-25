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