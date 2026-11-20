#!/usr/bin/env python3
"""
MediLink Enterprise — Local Preview Server
A zero-dependency HTTP server to run MediLink locally.

Usage:
    python server.py
    python server.py 8080
"""

import http.server
import socketserver
import webbrowser
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MediLinkHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[MediLink] {self.address_string()} - {format % args}\n")

def run():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), MediLinkHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 64)
        print("  MediLink: Aadhaar-Based Unified Medical Records System")
        print("  Enterprise Hospital Management & Interoperability EMR")
        print("=" * 64)
        print(f"  > Server running at: {url}")
        print("  > Serving directory:", DIRECTORY)
        print("  > Press Ctrl+C to terminate the server.\n")

        # Open in default browser automatically
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[MediLink] Server stopped gracefully.")

if __name__ == "__main__":
    run()
