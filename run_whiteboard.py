#!/usr/bin/env python3
"""
Smart Whiteboard Launcher
Launches the Streamlit-based Smart Whiteboard UI for AI-powered tutoring.
"""

import subprocess
import sys
import os

def main():
    """Launch the Smart Whiteboard Streamlit app."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    whiteboard_path = os.path.join(script_dir, "ui", "smart_whiteboard.py")
    
    # Check if the whiteboard file exists
    if not os.path.exists(whiteboard_path):
        print(f"❌ Error: Smart Whiteboard file not found at {whiteboard_path}")
        print("Please ensure the file exists and try again.")
        sys.exit(1)
    
    print("🚀 Launching Smart Whiteboard...")
    print("📝 This will open a web browser with the drawing interface.")
    print("💡 Draw equations, diagrams, or sketches for AI-powered tutoring!")
    print("🌐 The app will be available at: http://localhost:8501")
    print("\n" + "="*50)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            whiteboard_path,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Smart Whiteboard closed by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Smart Whiteboard: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: Streamlit not found.")
        print("Please install Streamlit:")
        print("  pip install streamlit streamlit-drawable-canvas")
        sys.exit(1)

if __name__ == "__main__":
    main() 