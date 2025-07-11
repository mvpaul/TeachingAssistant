#!/usr/bin/env python3
"""
React Frontend Launcher
Launches the React + Vite frontend for the Smart Whiteboard.
"""

import subprocess
import sys
import os
import platform

def check_node_installed():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def check_npm_installed():
    """Check if npm is installed."""
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def install_dependencies():
    """Install npm dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run(['npm', 'install'], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_dev_server():
    """Start the Vite development server."""
    print("🚀 Starting development server...")
    try:
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start development server: {e}")
    except KeyboardInterrupt:
        print("\n👋 Development server stopped.")

def get_installation_instructions():
    """Get installation instructions based on the platform."""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        return """
📋 Installation Instructions for macOS:

1. Install Homebrew (if not already installed):
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Install Node.js:
   brew install node

3. Verify installation:
   node --version
   npm --version

4. Run this script again:
   python3 run_frontend.py
"""
    elif system == "linux":
        return """
📋 Installation Instructions for Linux:

1. Install Node.js using your package manager:

   Ubuntu/Debian:
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt-get install -y nodejs

   CentOS/RHEL/Fedora:
   curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
   sudo yum install -y nodejs

2. Verify installation:
   node --version
   npm --version

3. Run this script again:
   python3 run_frontend.py
"""
    elif system == "windows":
        return """
📋 Installation Instructions for Windows:

1. Download Node.js from: https://nodejs.org/
2. Run the installer and follow the setup wizard
3. Restart your terminal/command prompt
4. Verify installation:
   node --version
   npm --version
5. Run this script again:
   python run_frontend.py
"""
    else:
        return """
📋 Installation Instructions:

1. Download Node.js from: https://nodejs.org/
2. Follow the installation instructions for your platform
3. Verify installation:
   node --version
   npm --version
4. Run this script again
"""

def main():
    """Main launcher function."""
    print("🎨 Smart Whiteboard Frontend Launcher")
    print("=" * 50)
    
    # Check if Node.js is installed
    if not check_node_installed():
        print("❌ Node.js is not installed.")
        print(get_installation_instructions())
        return
    
    # Check if npm is installed
    if not check_npm_installed():
        print("❌ npm is not installed.")
        print(get_installation_instructions())
        return
    
    # Get Node.js and npm versions
    try:
        node_version = subprocess.run(['node', '--version'], 
                                    capture_output=True, text=True).stdout.strip()
        npm_version = subprocess.run(['npm', '--version'], 
                                   capture_output=True, text=True).stdout.strip()
        print(f"✅ Node.js {node_version} and npm {npm_version} are installed")
    except Exception as e:
        print(f"⚠️  Could not get version info: {e}")
    
    # Check if package.json exists
    if not os.path.exists('package.json'):
        print("❌ package.json not found. Make sure you're in the correct directory.")
        return
    
    # Check if node_modules exists
    if not os.path.exists('node_modules'):
        print("📦 node_modules not found. Installing dependencies...")
        if not install_dependencies():
            return
    else:
        print("✅ Dependencies already installed")
    
    # Start the development server
    print("\n🌐 The frontend will be available at: http://localhost:3000")
    print("📱 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    start_dev_server()

if __name__ == "__main__":
    main() 