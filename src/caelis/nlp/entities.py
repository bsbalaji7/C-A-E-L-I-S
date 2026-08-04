import re


APPLICATIONS = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "msedge",
    "microsoft edge": "msedge",
    "firefox": "firefox",
    "notepad": "notepad",
    "paint": "mspaint",
    "calculator": "calc",
    "calc": "calc",
    "cmd": "cmd",
    "command prompt": "cmd",
    "powershell": "powershell",
    "explorer": "explorer",
    "file explorer": "explorer",
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
    "spotify": "spotify",
    "discord": "discord",
    "steam": "steam",
}

def extract_app(text: str):
    """
    Backward compatibility for old matcher.py
    """

    entities = extract_entities(text)

    return entities.get("application")

def extract_entities(text: str) -> dict:
    """
    Extract entities from a user command.

    Example:
        "open chrome"
            ->
        {"application": "chrome"}

        "close vscode"
            ->
        {"application": "code"}
    """

    entities = {}

    if not text:
        return entities

    sentence = text.lower()

    

    # -------------------------------
    # Application Detection
    # -------------------------------

    for name, executable in APPLICATIONS.items():

        if re.search(r"\b" + re.escape(name) + r"\b", sentence):

            entities["application"] = executable
            break

    return entities