# C.A.E.L.I.S.

> **Cognitive Autonomous Entity with Lucidity, Intelligence & Synthesis**

**CAELIS** is a Python-based intelligent desktop assistant designed to operate as a system-resident AI companion. Inspired by futuristic assistants such as JARVIS and FRIDAY, CAELIS aims to combine conversational intelligence, voice interaction, multilingual understanding, memory, and safe computer automation into one modular system.

---

## 🚀 Vision

CAELIS is being developed as more than a chatbot.

The goal is to create an intelligent assistant that can:

* Communicate naturally with the user
* Understand text and voice commands
* Interact with the operating system
* Open applications, files, and websites
* Remember useful information and conversation context
* Understand multiple languages
* Interpret Tamil written using English characters (Tanglish)
* Automate repetitive computer tasks
* Provide system information
* Run continuously as a desktop assistant
* Respond intelligently based on context
* Protect sensitive system actions through permission checks

---

## ✨ Core Features

### 🧠 Intelligent Assistant

CAELIS processes user requests through a modular intelligence pipeline consisting of:

* Natural Language Processing
* Intent Detection
* Entity Extraction
* Context Understanding
* Response Generation
* Action Routing

Example:

```text
User: Open Chrome

Intent: OPEN_APP
Entity: chrome

CAELIS: Opening Chrome.
```

---

### 🖥️ System Control

CAELIS is designed to interact directly with the computer.

Planned capabilities include:

* Open and close applications
* Open files and folders
* Launch websites
* Search the web
* Read system information
* Monitor CPU and memory usage
* Control system volume
* Clipboard operations
* Keyboard automation
* Mouse automation
* Process management
* Notifications
* Safe power controls

Sensitive actions will pass through a security and permission layer before execution.

---

## 🎙️ Voice Interaction

CAELIS will support hands-free interaction using:

```text
Voice
  ↓
Speech-to-Text
  ↓
Language Detection
  ↓
NLP
  ↓
Intent Detection
  ↓
CAELIS Brain
  ↓
Action
  ↓
Response
  ↓
Text-to-Speech
```

Planned voice capabilities include:

* Speech recognition
* Text-to-speech
* Wake-word detection
* Continuous assistant mode
* Multilingual voice commands

---

## 🌍 Multilingual Support

CAELIS is designed to support:

| Language | Status         |
| -------- | -------------- |
| English  | 🚧 Development |
| Tamil    | 📋 Planned     |
| Tanglish | 📋 Planned     |
| Telugu   | 📋 Planned     |
| German   | 📋 Planned     |

### Tanglish Support

Tanglish allows Tamil commands to be written or spoken using English characters.

```text
User:
Chrome open pannu

CAELIS:
Sure, Chrome open panren.
```

Native Tamil:

```text
User:
குரோம் திற

CAELIS:
குரோம் திறக்கிறேன்.
```

English:

```text
User:
Open Chrome

CAELIS:
Opening Chrome.
```

Different languages should ultimately resolve to the same underlying intent:

```text
Open Chrome
Chrome open pannu
குரோம் திற

       ↓

Intent: OPEN_APP
Entity: chrome
```

---

## 🧠 CAELIS Architecture

```text
                     CAELIS
                       │
                  User Input
                  /        \
               Text        Voice
                │            │
                │      Speech-to-Text
                └──────┬─────┘
                       ↓
              Language Detection
                       ↓
                 NLP Processor
                       ↓
              Intent + Entities
                       ↓
                  CAELIS Brain
                       ↓
                  Action Router
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       System       Services      Memory
       Control                     System
          │            │            │
          └────────────┼────────────┘
                       ↓
                Response Engine
                       ↓
                  Text / Voice
```

---

## 📁 Project Structure

```text
CAELIS/
│
├── main.py
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── caelis/
│   ├── core/
│   │   ├── brain.py
│   │   ├── intent.py
│   │   ├── router.py
│   │   ├── context.py
│   │   └── response.py
│   │
│   ├── intelligence/
│   │   ├── nlp/
│   │   ├── ml/
│   │   ├── dl/
│   │   └── models/
│   │
│   ├── languages/
│   │   ├── detector.py
│   │   ├── translator.py
│   │   ├── normalizer.py
│   │   ├── english.py
│   │   ├── tamil.py
│   │   ├── tanglish.py
│   │   ├── telugu.py
│   │   └── german.py
│   │
│   ├── voice/
│   │   ├── listener.py
│   │   ├── speaker.py
│   │   ├── speech_to_text.py
│   │   ├── text_to_speech.py
│   │   └── wake_word.py
│   │
│   ├── system/
│   │   ├── app_control.py
│   │   ├── file_control.py
│   │   ├── browser_control.py
│   │   ├── system_info.py
│   │   ├── process_manager.py
│   │   ├── volume_control.py
│   │   └── automation.py
│   │
│   ├── memory/
│   │   ├── database.py
│   │   ├── memory_manager.py
│   │   ├── conversation_memory.py
│   │   └── preference_memory.py
│   │
│   ├── security/
│   │   ├── permissions.py
│   │   ├── action_guard.py
│   │   ├── command_validator.py
│   │   └── audit_logger.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── chat_widget.py
│   │   ├── voice_widget.py
│   │   └── system_tray.py
│   │
│   ├── services/
│   ├── startup/
│   ├── config/
│   └── utils/
│
├── data/
├── models/
├── assets/
├── logs/
├── scripts/
├── tests/
└── docs/
```

---

## 🛠️ Technology Stack

### Core

* Python 3
* Object-Oriented Programming
* Async processing where appropriate

### Desktop Interface

* PySide6 / Qt

### Artificial Intelligence

* Natural Language Processing
* Machine Learning
* Deep Learning
* Pretrained AI models
* Intent classification
* Entity extraction

### Voice

* Speech-to-Text
* Text-to-Speech
* Wake-word recognition

### Memory

* SQLite
* Local conversation storage
* Context management
* Preference storage

### Automation

* Python system APIs
* PyAutoGUI
* Windows APIs
* Process management

---

## 🔄 Command Processing

A command such as:

```text
Caelis, Notepad open pannu
```

will move through:

```text
Input
  ↓
Language Detection
  ↓
Tanglish Normalization
  ↓
Intent Detection
  ↓
Entity Extraction
  ↓
Intent: OPEN_APP
Entity: notepad
  ↓
Security Check
  ↓
Action Router
  ↓
App Controller
  ↓
Windows
  ↓
Notepad Opens
  ↓
Response
```

---

## 🛡️ Security

System automation requires careful permission management.

CAELIS is being designed around a **safe-action-first** architecture.

Actions can be classified into levels such as:

```text
SAFE
│
├── Open application
├── Read system information
└── Open website

CONFIRMATION REQUIRED
│
├── Close important processes
├── Modify files
├── Delete files
└── Change system settings

RESTRICTED
│
├── Dangerous shell commands
├── Unauthorized privilege changes
└── Security-sensitive operations
```

CAELIS should request confirmation before performing destructive or sensitive operations.

---

## 🧠 Memory System

CAELIS will eventually support different forms of memory:

```text
Memory
│
├── Conversation Memory
├── Context Memory
├── Preference Memory
└── Persistent Memory
```

The objective is to allow conversations such as:

```text
User:
Open my project folder.

CAELIS:
Which project?

User:
Caelis.

CAELIS:
Opening your Caelis project folder.
```

Instead of treating every message as an isolated command.

---

## 🗺️ Development Roadmap

### Phase 1 — Foundation

* [ ] Project architecture
* [ ] CAELIS Brain
* [ ] Intent system
* [ ] Action router
* [ ] Basic command processing

### Phase 2 — System Control

* [ ] Application control
* [ ] File/folder control
* [ ] Browser control
* [ ] System information
* [ ] Process management
* [ ] Safe automation

### Phase 3 — Language Intelligence

* [ ] English processing
* [ ] Tamil processing
* [ ] Tanglish processing
* [ ] Telugu processing
* [ ] German processing
* [ ] Automatic language detection

### Phase 4 — Voice

* [ ] Speech-to-text
* [ ] Text-to-speech
* [ ] Voice command processing
* [ ] Wake-word system

### Phase 5 — Memory

* [ ] SQLite database
* [ ] Conversation history
* [ ] Context memory
* [ ] User preferences
* [ ] Persistent memory

### Phase 6 — AI

* [ ] NLP pipeline
* [ ] Intent classification
* [ ] Entity extraction
* [ ] Pretrained models
* [ ] Conversational intelligence
* [ ] Context-aware responses

### Phase 7 — Desktop UI

* [ ] PySide6 interface
* [ ] Chat interface
* [ ] Voice interface
* [ ] Settings
* [ ] System tray
* [ ] Notifications

### Phase 8 — System Integration

* [ ] Start with Windows
* [ ] Background mode
* [ ] Wake-word activation
* [ ] Permission management
* [ ] Logging
* [ ] Packaging

---

## 🎯 Example Commands

```text
Hello Caelis

Open Notepad

Open Chrome

Chrome open pannu

குரோம் திற

Open my Downloads folder

What's my CPU usage?

What's my battery percentage?

Increase the volume

Search for Python tutorials

Open my Caelis project

Caelis, system status sollu
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-caelis-repository-url>
cd CAELIS
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment configuration:

```text
.env.example → .env
```

Run CAELIS:

```bash
python main.py
```

---

## ⚠️ Development Status

> **CAELIS is currently under active development.**

Features described in this README represent both implemented and planned functionality. The project should not yet be considered production-ready.

---

## 🤝 Contributing

CAELIS is currently an experimental personal AI-assistant project.

Contributions, ideas, bug reports, and feature suggestions may be welcomed as development progresses.

---

## 📜 License

License information will be added as the project develops.

---

## 👨‍💻 Author

**BS**

Creator & Developer of **C.A.E.L.I.S.**

---

## ⭐ Project Goal

The long-term objective of CAELIS is simple:

> **Build an intelligent assistant that doesn't just answer — it understands, remembers, communicates, and acts.**

**C.A.E.L.I.S.**
*Cognitive Autonomous Entity with Lucidity, Intelligence & Synthesis*
