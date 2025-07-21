# 🔧 Google API Setup Guide

Follow these steps to set up Google API credentials for the Calendar & Tasks Assistant.

## Step 1: Google Cloud Console Setup

1. **Open Google Cloud Console** (already opened for you)
   - Go to: https://console.cloud.google.com/

2. **Create or Select Project**
   - Click "Select a project" at the top
   - Either select an existing project or click "New Project"
   - If creating new: Enter project name (e.g., "calendar-tasks-app")
   - Click "Create"

## Step 2: Enable Required APIs

1. **Go to API Library**
   - In the left sidebar, click "APIs & Services" > "Library"
   - Or go directly to: https://console.cloud.google.com/apis/library

2. **Enable Google Calendar API**
   - Search for "Google Calendar API"
   - Click on it and click "Enable"

3. **Enable Google Tasks API**
   - Search for "Google Tasks API"  
   - Click on it and click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. **Go to Credentials Page**
   - In the left sidebar, click "APIs & Services" > "Credentials"
   - Or go directly to: https://console.cloud.google.com/apis/credentials

2. **Configure OAuth Consent Screen** (if prompted)
   - Click "OAuth consent screen"
   - Choose "External" (unless you have a Google Workspace account)
   - Fill in required fields:
     - App name: "Calendar Tasks Assistant"
     - User support email: your email
     - Developer contact: your email
   - Click "Save and Continue"
   - Add scopes (optional for testing)
   - Add test users (add your email)
   - Click "Save and Continue"

3. **Create OAuth 2.0 Client ID**
   - Go back to "Credentials" tab
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Name: "Calendar Tasks Assistant"
   - **Authorized redirect URIs**: Add `http://localhost:8501`
   - Click "Create"

4. **Copy Your Credentials**
   - A popup will show your Client ID and Client Secret
   - **IMPORTANT**: Copy both values - you'll need them next

## Step 4: Configure the App

Once you have your credentials, you have two options:

### Option A: Manual Configuration
1. Open `.streamlit/secrets.toml` in a text editor
2. Replace the placeholder values:
   ```toml
   CLIENT_ID = "your-actual-client-id-here.apps.googleusercontent.com"
   CLIENT_SECRET = "your-actual-client-secret-here"
   REDIRECT_URI = "http://localhost:8501"
   ```

### Option B: Use Quick Setup Script
1. Run: `python quick_setup.py`
2. Paste your Client ID and Client Secret when prompted

## Step 5: Run the App

1. **Start the application**:
   ```bash
   python -m streamlit run app.py
   ```

2. **First-time authentication**:
   - Click "Click here to login with Google"
   - Sign in with your Google account
   - Grant permissions for Calendar and Tasks access
   - You'll be redirected back to the app

3. **Start using the app**:
   - Dashboard: View today's events and tasks
   - Calendar Events: Manage your calendar
   - Tasks: Manage your Google Tasks

## Troubleshooting

### Common Issues:

1. **"OAuth client not found"**
   - Make sure you copied the correct Client ID
   - Verify the redirect URI is exactly `http://localhost:8501`

2. **"Access blocked"**
   - Your app needs to be verified by Google for production use
   - For testing, add your email as a test user in OAuth consent screen

3. **"Secrets not found"**
   - Make sure `.streamlit/secrets.toml` exists in the project directory
   - Check that the file has the correct format

4. **"API not enabled"**
   - Verify both Google Calendar API and Google Tasks API are enabled
   - Wait a few minutes after enabling APIs

### Quick Links:
- Google Cloud Console: https://console.cloud.google.com/
- API Library: https://console.cloud.google.com/apis/library
- Credentials: https://console.cloud.google.com/apis/credentials
- OAuth Consent: https://console.cloud.google.com/apis/credentials/consent

## Security Notes

- Keep your Client Secret private
- Don't commit secrets.toml to version control
- The app only requests necessary permissions (Calendar and Tasks)
- Your data stays between you and Google - the app doesn't store anything

---

**Need help?** Check the troubleshooting section above or refer to the Google Cloud documentation.
