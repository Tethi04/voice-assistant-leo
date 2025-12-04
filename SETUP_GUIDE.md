# 🚀 LEO ASSISTANT - SETUP GUIDE

## 📋 Prerequisites
- **Python 3.8, 3.9, 3.10, or 3.11** (NOT Python 3.13 - it has compatibility issues)
- Microphone (for voice features)
- Internet connection (for online features)

## 🛠️ Installation Steps

### 1. Install Python
Download from: https://python.org/downloads
- Choose version 3.10 or 3.11
- ✅ **IMPORTANT**: Check "Add Python to PATH" during installation

### 2. Download Leo Assistant
- Go to: https://github.com/Tethi04/voice-assistant-leo
- Click "Code" → "Download ZIP"
- Extract to Desktop

### 3. Open Command Prompt
1. Open the `voice-assistant-leo` folder
2. Click in the address bar
3. Type `cmd` and press Enter

### 4. Install Dependencies
```cmd
# Install basic dependencies
pip install -r requirements.txt

# For Windows microphone support
pip install pipwin
pipwin install pyaudio

# If any errors, install individually:
pip install SpeechRecognition==3.10.0
pip install pyttsx3==2.90
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
