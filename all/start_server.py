#!/usr/bin/env python3
"""
Simple HTTP server for running Ashes of Aether locally.
This provides better performance than opening the HTML file directly.
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port=8000):
    """Run the HTTP server and open the game in browser."""
    with socketserver.TCPServer(("", port), GameHTTPRequestHandler) as httpd:
        print(f"🚀 Ashes of Aether server running at:")
        print(f"   http://localhost:{port}")
        print(f"   Press Ctrl+C to stop the server")
        print(f"\n🌐 Opening game in browser...")
        
        # Open the game in default browser
        webbrowser.open(f"http://localhost:{port}")
        
        # Start serving
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()  # Start the server on the default port 8000
