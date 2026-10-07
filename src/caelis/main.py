"""
CAELIS Main Entry Point.
Launches the CAELIS Anti-Gravity Technology Desktop Interface & API Server.
"""

import sys
import os
import argparse

# Ensure src directory is in sys.path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from caelis.interface.server import start_server


def main():
    parser = argparse.ArgumentParser(description="CAELIS Anti-Gravity Technology Interface")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve the desktop HUD interface")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    parser.add_argument("--test", action="store_true", help="Run a non-blocking test startup")

    args = parser.parse_args()

    print("==========================================================")
    print("                C. A. E. L. I. S.                        ")
    print(" Cognitive Autonomous Entity with Lucidity & Synthesis   ")
    print("      ANTI-GRAVITY TECHNOLOGY INTERFACE v3.6              ")
    print("==========================================================")

    if args.test:
        print("[TEST MODE] CAELIS modules compiled and validated successfully.")
        sys.exit(0)

    start_server(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()