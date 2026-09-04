"""
Python HTTP & API Desktop Server Handler for CAELIS HUD Interface.
Serves static WebGL HUD assets and exposes REST endpoints for system status and NLP intent resolution.
"""

import http.server
import socketserver
import webbrowser
import os
import json
import urllib.parse
from typing import Tuple
from caelis.nlp.antigrav_intent import parse_antigrav_command

PORT = 8080
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")


class CaelisHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # REST API: Status check
        if parsed_path.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_data = {
                "status": "ONLINE",
                "system": "CAELIS Anti-Gravity Core v3.6",
                "quantum_matrix": "STABLE",
                "wake_word": "CAELIS",
                "supported_languages": ["English", "Thanglish", "Tamil"],
            }
            self.wfile.write(json.dumps(status_data).encode("utf-8"))
            return

        # Serve static assets
        return super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # REST API: Process voice command string
        if parsed_path.path == "/api/parse-command":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                cmd_text = payload.get("command", "")
                result = parse_antigrav_command(cmd_text)

                response_data = {
                    "matched": result.matched,
                    "intent": result.name,
                    "confidence": result.confidence,
                    "matched_pattern": result.matched_pattern,
                    "entities": result.entities,
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return

        self.send_response(404)
        self.end_headers()


def start_server(port: int = PORT, open_browser: bool = True):
    # Try finding an open port if 8080 is busy
    actual_port = port
    handler = CaelisHTTPRequestHandler

    while actual_port < port + 20:
        try:
            with socketserver.TCPServer(("127.0.0.1", actual_port), handler) as httpd:
                url = f"http://127.0.0.1:{actual_port}"
                print(f"[CAELIS ENGINE] HUD Server listening at {url}")

                if open_browser:
                    print(f"[CAELIS ENGINE] Opening desktop HUD window...")
                    webbrowser.open(url)

                httpd.serve_forever()
                break
        except OSError:
            actual_port += 1


if __name__ == "__main__":
    start_server()
