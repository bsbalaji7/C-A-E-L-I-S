APP_ALIASES = {
    "chrome": "chrome",
    "google chrome": "chrome",

    "notepad": "notepad",
    "note pad": "notepad",

    "calculator": "calculator",
    "calc": "calculator",

    "vscode": "vscode",
    "vs code": "vscode",
    "visual studio code": "vscode",

    "explorer": "explorer",
    "file explorer": "explorer",

    "cmd": "cmd",
    "command prompt": "cmd",

    "powershell": "powershell",
}


def extract_app(text: str) -> str | None:
    text = text.lower().strip()

    # Longer aliases first.
    for alias in sorted(
        APP_ALIASES,
        key=len,
        reverse=True,
    ):
        if alias in text:
            return APP_ALIASES[alias]

    return None