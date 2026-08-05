import os
import subprocess
import platform


class Executor:
    """
    Executes safe system commands.
    """

    def __init__(self):
        self.os_name = platform.system().lower()

    # -----------------------------------------------------
    # OPEN APPLICATION
    # -----------------------------------------------------

    def open_application(self, app: str) -> bool:

        try:

            windows_apps = {
                "chrome": "start chrome",
                "msedge": "start msedge",
                "firefox": "start firefox",
                "code": "code",
                "notepad": "notepad",
                "calc": "calc",
                "mspaint": "mspaint",
                "cmd": "cmd",
                "powershell": "powershell",
                "explorer": "explorer",
                "spotify": "spotify",
                "discord": "discord",
                "steam": "steam",
            }

            command = windows_apps.get(app)

            if not command:
                return False

            if command.startswith("start "):
                os.system(command)
            else:
                subprocess.Popen(command.split())

            return True

        except Exception as e:
            print("[EXECUTOR]", e)
            return False

    # -----------------------------------------------------
    # CLOSE APPLICATION
    # -----------------------------------------------------

    def close_application(self, app: str) -> bool:

        try:

            process_names = {
                "chrome": "chrome.exe",
                "msedge": "msedge.exe",
                "firefox": "firefox.exe",
                "code": "Code.exe",
                "notepad": "notepad.exe",
                "calc": "CalculatorApp.exe",
                "mspaint": "mspaint.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "spotify": "Spotify.exe",
                "discord": "Discord.exe",
                "steam": "steam.exe",
            }

            process = process_names.get(app)

            if not process:
                return False

            os.system(f'taskkill /IM "{process}" /F')

            return True

        except Exception as e:
            print("[EXECUTOR]", e)
            return False