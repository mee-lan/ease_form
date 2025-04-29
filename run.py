#!/usr/bin/env python3
"""
Run script for Nepal Forms Assistant Chrome Extension
This script runs the backend server for the Chrome extension.
"""

import os
import sys
import subprocess
import webbrowser
import time
import argparse

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def run_backend_server(debug=False):
    """Run the backend Flask server"""
    print_header("Starting Backend Server")
    
    # Check if Python requirements are installed
    try:
        import flask
        import google.generativeai
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        print(f"Error: Missing required packages - {e}")
        print("Installing requirements...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
            print("Requirements installed successfully!")
        except subprocess.CalledProcessError:
            print("Failed to install requirements. Please install them manually:")
            print("  pip install -r backend/requirements.txt")
            return
    
    # Check if the data directory exists
    backend_data_dir = os.path.join("backend", "data")
    if not os.path.exists(backend_data_dir):
        print(f"Creating data directory: {backend_data_dir}")
        os.makedirs(backend_data_dir, exist_ok=True)
    
    # Check if forms data exists
    forms_json_path = os.path.join(backend_data_dir, "forms.json")
    if not os.path.exists(forms_json_path):
        print("Forms data not found. Running initialization script...")
        try:
            from init import initialize_form_data
            initialize_form_data()
        except ImportError:
            print("Failed to import initialization script.")
            print("Please run init.py first: python init.py")
            return
    
    # Run the Flask server
    server_script = os.path.join("backend", "server.py")
    
    # Check if server script exists
    if not os.path.exists(server_script):
        print(f"Error: Server script not found at {server_script}")
        return
    
    print(f"Running server: {server_script}")
    
    # Build the command to run the server
    cmd = [sys.executable, server_script]
    
    # Run server in debug mode if requested
    if debug:
        os.environ["FLASK_ENV"] = "development"
        os.environ["FLASK_DEBUG"] = "1"
    
    try:
        # Print server startup message
        print("\nBackend server is starting at http://localhost:5000")
        print("Press Ctrl+C to stop the server\n")
        
        # Run the server process
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nError running server: {e}")

def open_chrome_extensions():
    """Open Chrome extensions page"""
    extensions_url = "chrome://extensions/"
    
    print(f"Opening {extensions_url} in Chrome...")
    
    try:
        # Try to open Chrome with the extensions page
        # This might not work on all systems due to chrome:// protocol restrictions
        webbrowser.get("chrome").open(extensions_url)
    except Exception:
        print("Could not automatically open Chrome extensions page.")
        print("\nTo load the extension in Chrome:")
        print("  1. Open Chrome and go to chrome://extensions/")
        print("  2. Enable Developer mode (top right)")
        print("  3. Click 'Load unpacked' and select this directory")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run the Nepal Forms Assistant backend server")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--chrome", action="store_true", help="Open Chrome extensions page")
    
    args = parser.parse_args()
    
    print_header("Nepal Forms Assistant - Run Script")
    
    # Open Chrome extensions page if requested
    if args.chrome:
        open_chrome_extensions()
    
    # Run the backend server
    run_backend_server(debug=args.debug)

if __name__ == "__main__":
    main() 