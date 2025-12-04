@echo off
echo ====================================
echo    LEO ASSISTANT - WINDOWS SETUP
echo ====================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from python.org
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo.
echo Step 2: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 3: Installing required packages...
pip install SpeechRecognition==3.10.0
pip install pyttsx3==2.90
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2

echo.
echo Step 4: Installing PyAudio for voice input...
pip install pipwin
pipwin install pyaudio

echo.
echo Step 5: Creating .env file for API keys...
if not exist .env (
    copy config\api_keys.template .env
    echo Created .env file
    echo Please edit .env to add your API keys
) else (
    echo .env file already exists
)

echo.
echo ====================================
echo    SETUP COMPLETE!
echo ====================================
echo.
echo To run Leo Assistant:
echo 1. For OFFLINE mode: python main.py
echo 2. For ONLINE mode: Add API keys to .env file
echo.
echo Press any key to exit...
pause > nul
