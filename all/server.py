#!/usr/bin/env python3
"""
Simple HTTP server for running Ashes of Aether locally.
This provides better performance than opening the HTML file directly.
"""

import http.server
import socketserver
import webbrowser
import os
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
    try:
        with socketserver.TCPServer(("", port), GameHTTPRequestHandler) as httpd:
            print(f"🚀 Ashes of Aether server running at:")
            print(f"   http://localhost:{port}")
            print(f"   Press Ctrl+C to stop the server")
            print(f"\n🌐 Opening game in browser...")
            
            # Open the game in default browser
            webbrowser.open(f"http://localhost:{port}")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    import sys
    
    # Get port from command line argument or use default
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid port number: {sys.argv[1]}, using default port 8000")
    
    print("🎮 Starting Ashes of Aether Local Server")
    print("=" * 50)
    
    # Check if index.html exists
    if not Path("index.html").exists():
        print("❌ Error: index.html not found in current directory")
        print("💡 Make sure you're running this script from the game directory")
        exit(1)
    
    run_server(port)
