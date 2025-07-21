#!/usr/bin/env python3
"""
Quick setup script for Google Calendar & Tasks Assistant
Run this if you already have Google API credentials
"""

import os
from pathlib import Path

def main():
    print("🚀 Quick Setup - Google Calendar & Tasks Assistant")
    print("=" * 50)
    
    secrets_path = Path(".streamlit/secrets.toml")
    
    print("Please enter your Google API credentials:")
    print("(Get these from https://console.cloud.google.com/apis/credentials)")
    print()
    
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Please provide both Client ID and Client Secret")
        return
    
    # Create secrets content
    secrets_content = f'''# Google API Credentials
CLIENT_ID = "{client_id}"
CLIENT_SECRET = "{client_secret}"
REDIRECT_URI = "http://localhost:8501"
'''
    
    try:
        # Ensure directory exists
        secrets_path.parent.mkdir(exist_ok=True)
        
        # Write secrets file
        with open(secrets_path, 'w') as f:
            f.write(secrets_content)
        
        print()
        print("✅ Credentials saved successfully!")
        print()
        print("🚀 To start the app, run:")
        print("   python -m streamlit run app.py")
        print()
        print("📝 First time setup:")
        print("   1. Click the Google login link in the app")
        print("   2. Grant Calendar and Tasks permissions")
        print("   3. You'll be redirected back to the app")
        
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")

if __name__ == "__main__":
    main()
