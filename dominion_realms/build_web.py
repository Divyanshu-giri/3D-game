#!/usr/bin/env python3
"""
Build script for Dominion Realms web version using Pygbag
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_web_version():
    print("Building Dominion Realms Web Version...")
    
    # Check if pygbag is installed
    try:
        import pygbag
        print("✓ Pygbag is installed")
    except ImportError:
        print("✗ Pygbag not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygbag"])
    
    # Create build directory
    build_dir = Path("build/web")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy necessary files
    files_to_copy = [
        "web_main.py",
        "config.py",
        "requirements.txt",
        "index.html"
    ]
    
    directories_to_copy = [
        "player",
        "physics_engine", 
        "world",
        "ui",
        "boss"
    ]
    
    print("Copying files...")
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, build_dir / file)
            print(f"✓ Copied {file}")
        else:
            print(f"✗ Missing {file}")
    
    # Copy directories
    for directory in directories_to_copy:
        src_dir = Path(directory)
        dest_dir = build_dir / directory
        if src_dir.exists():
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(src_dir, dest_dir)
            print(f"✓ Copied {directory}/")
        else:
            print(f"✗ Missing {directory}/")
    
    # Create assets directory (empty for now)
    assets_dir = build_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Create pygbag config
    pygbag_config = """
[pygbag]
main = "web_main.py"
assets = "assets"
width = 1024
height = 768
fullscreen = false
debug = true
    """
    
    with open(build_dir / "pygbag.toml", "w") as f:
        f.write(pygbag_config)
    
    print("Building with Pygbag...")
    
    # Change to build directory and run pygbag
    original_dir = os.getcwd()
    os.chdir(build_dir)
    
    try:
        # Build the web version
        result = subprocess.run([
            sys.executable, "-m", "pygbag", 
            "--build", 
            "--template", "index.html",
            "web_main.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Web build successful!")
            print("Files are in build/web/")
            
            # Create a simple server for testing
            create_test_server(build_dir)
            
        else:
            print("✗ Build failed:")
            print(result.stderr)
            
    except Exception as e:
        print(f"✗ Build error: {e}")
    finally:
        os.chdir(original_dir)

def create_test_server(build_dir):
    """Create a simple test server script"""
    server_script = """#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8000
WEB_DIR = "."

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

def run_server():
    with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Open this URL in a web browser to test the game")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nServer stopped")

if __name__ == "__main__":
    run_server()
"""
    
    with open(build_dir / "test_server.py", "w") as f:
        f.write(server_script)
    
    print("✓ Created test server script: test_server.py")
    print("Run 'python test_server.py' to test the web version locally")

def create_apk_build_script():
    """Create a script for building APK (placeholder)"""
    apk_script = """#!/usr/bin/env python3
# APK build script for Dominion Realms
# This requires additional setup with Buildozer or similar tools

print("APK build setup for Dominion Realms")
print("This requires:")
print("1. Android SDK installed")
print("2. Buildozer configured")
print("3. Additional Android dependencies")

# For now, this is a placeholder
# Actual APK build would require converting to Kivy or using pygame-subset for Android
"""
    
    with open("build_apk.py", "w") as f:
        f.write(apk_script)
    
    print("✓ Created APK build script placeholder: build_apk.py")

if __name__ == "__main__":
    build_web_version()
    create_apk_build_script()
    
    print("\\nNext steps:")
    print("1. Run 'python build_web.py' to build the web version")
    print("2. cd build/web && python test_server.py to test locally")
    print("3. Check build_apk.py for Android APK build instructions")
