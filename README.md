# **🎤 Leo - Voice Controlled Assistant**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Offline](https://img.shields.io/badge/Offline-Supported-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Web](https://img.shields.io/badge/Web-Demo-9cf)

**A smart voice assistant that works both online and offline with web demo support**

[Live Web Demo](https://voice-assistant-leo-bte3ynpwrbtf3seehdzhjc.streamlit.app/) •
[GitHub Pages](https://tethi04.github.io/voice-assistant-leo/) •
[GitHub Repo](https://github.com/Tethi04/voice-assistant-leo)

</div>

## ✨ **Features**

### 🎤 **Voice & Audio Features**
- **Real-time Voice Recognition** using Web Speech API (browser) and SpeechRecognition (Python)
- **Text-to-Speech Responses** with adjustable voice settings
- **Microphone Integration** for seamless voice commands
- **Dual Mode**: Works both online and offline

### 🌐 **Web & API Integration**
- **Live Weather Updates** using OpenWeatherMap API
- **Latest News Headlines** via NewsAPI
- **Web Search** functionality
- **Streamlit Web Demo** with full voice support

### 💾 **Productivity Tools**
- **Smart Notes System** - Remember and retrieve important information
- **App Control** - Open calculator, notepad, and other applications
- **System Integration** - Works with your operating system
- **Time & Date** - Always accurate with timezone support

### 🔧 **Technical Capabilities**
- **Cross-Platform** - Windows, macOS, Linux compatible
- **Python 3.8-3.13 Support** with compatibility fixes
- **Modular Architecture** - Easy to extend and customize
- **Error Handling** - Graceful fallbacks and user-friendly messages

## 🚀 **Quick Start**

### **Option 1: Web Demo (No Installation)**
Visit our live demos:
- **🎤 Interactive Voice Demo**: [Streamlit App](https://voice-assistant-leo-bte3ynpwrbtf3seehdzhjc.streamlit.app/)
- **📱 Web Interface**: [GitHub Pages](https://tethi04.github.io/voice-assistant-leo/)

### **Option 2: Local Installation**

#### **Prerequisites**
- Python 3.8, 3.9, 3.10, or 3.11 (Recommended: Python 3.10)
- Microphone (for voice features)
- Internet connection (for online features)

#### **Installation Steps**

**Windows:**
```cmd
# 1. Clone the repository
git clone https://github.com/Tethi04/voice-assistant-leo.git
cd voice-assistant-leo

# 2. Install dependencies
pip install -r requirements.txt

# 3. For microphone support (Windows)
pip install pipwin
pipwin install pyaudio

# 4. Run Leo
python main.py
```

**macOS/Linux:**
```bash
# 1. Clone the repository
git clone https://github.com/Tethi04/voice-assistant-leo.git
cd voice-assistant-leo

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Install audio dependencies
# macOS:
brew install portaudio
# Linux (Ubuntu/Debian):
sudo apt-get install portaudio19-dev python3-pyaudio

# 4. Run Leo
python3 main.py
```

### **Option 3: Using Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Leo
python main.py
```

## 🎯 **Voice Commands**

### **📅 Time & Information**
- `"Hello Leo"` - Greeting
- `"What time is it?"` - Current time with timezone
- `"What's the date?"` - Today's date
- `"What can you do?"` - List available commands

### 😄 **Entertainment**
- `"Tell me a joke"` - Random jokes
- `"Another joke"` - More humor
- `"Make me laugh"` - Funny responses

### 🌤️ **Weather (Requires API Key)**
- `"What's the weather?"` - Your location weather
- `"Weather in London"` - Specific city weather
- `"Temperature in Delhi"` - Temperature only
- `"Is it raining?"` - Precipitation check

### 📰 **News (Requires API Key)**
- `"What's the news?"` - Top 5 headlines
- `"Latest news"` - Recent updates
- `"Breaking news"` - Urgent news

### 🔍 **Web & Apps**
- `"Search for Python tutorials"` - Google search
- `"Open calculator"` - Opens calculator app
- `"Open notepad"` - Opens text editor
- `"Open browser"` - Launches web browser

### 💾 **Productivity**
- `"Remember buy milk"` - Add note
- `"What are my notes?"` - View all notes
- `"Note: meeting at 3 PM"` - Quick note taking
- `"Remind me to call mom"` - Set reminder

### 🛑 **Control**
- `"Stop listening"` - Pause assistant
- `"Go to sleep"` - Enter sleep mode
- `"Wake up"` - Resume listening
- `"Exit"` or `"Goodbye"` - Shut down

## 🔧 **Configuration**

### **API Keys Setup (For Online Features)**

1. **Get Free API Keys:**
   - **Weather API**: [OpenWeatherMap](https://openweathermap.org/api) - Free tier available
   - **News API**: [NewsAPI](https://newsapi.org/register) - Free tier available

2. **Create `.env` file in project root:**
```env
OPENWEATHER_KEY=your_actual_openweather_api_key_here
NEWSAPI_KEY=your_actual_newsapi_key_here
```

**Note:** The `.env` file is for local use only and is excluded from Git via `.gitignore`

### **Python Version Compatibility**
- ✅ **Recommended**: Python 3.10 or 3.11
- ✅ **Works**: Python 3.8, 3.9
- ⚠️ **Limited**: Python 3.12 (some audio issues)
- ❌ **Not Recommended**: Python 3.13 (audio module compatibility issues)

## 🏗️ **Project Structure**

```
voice-assistant-leo/
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This documentation
├── requirements.txt              # Python dependencies
├── main.py                       # Main entry point (local app)
├── streamlit_app.py              # Web demo (Streamlit)
├── web_demo.html                 # Static web demo
├── SETUP_GUIDE.md                # Detailed setup guide
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── assistant.py              # Main assistant class
│   ├── commands.py               # Command handlers
│   ├── utils.py                  # Utility functions (time, weather, news, jokes)
│   └── config.py                 # Configuration loader with Python 3.13 fixes
│
├── config/                       # Configuration
│   └── api_keys.template         # API key template
│
└── tests/                        # Test files
    └── test_assistant.py         # Unit tests
```

## 🌐 **Web Deployment**

### **Streamlit Cloud Deployment**
1. **Requirements**: `streamlit_app.py` and `requirements.txt`
2. **Auto-deployment**: Push to GitHub → Streamlit detects changes
3. **Live at**: `https://voice-assistant-leo-bte3ynpwrbtf3seehdzhjc.streamlit.app/`

### **GitHub Pages Deployment**
1. **Static demo** available at: `https://tethi04.github.io/voice-assistant-leo/`
2. **No Python required** - Pure HTML/CSS/JavaScript
3. **Simulated voice experience** for demonstration

## 🔍 **Troubleshooting**

### **Common Issues & Solutions**

#### **"Microphone not found/working"**
```bash
# Test microphone
python -c "import speech_recognition as sr; print('Microphones:', sr.Microphone.list_microphone_names())"

# Windows specific:
# 1. Check Windows microphone settings
# 2. Give Python microphone permission
# 3. Run as Administrator
```

#### **"Module not found" Errors**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# Install individually if needed
pip install SpeechRecognition==3.10.0 pyttsx3==2.90 python-dotenv==1.0.0 requests==2.31.0 beautifulsoup4==4.12.2
```

#### **"PyAudio installation failed" (Windows)**
```cmd
# Use pipwin
pip install pipwin
pipwin install pyaudio

# OR download wheel manually:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

#### **Python 3.13 Users**
```python
# Add this fix to src/config.py at the top:
import sys
import types
if sys.version_info >= (3, 13):
    if 'aifc' not in sys.modules:
        aifc = types.ModuleType('aifc')
        aifc.Error = Exception
        sys.modules['aifc'] = aifc
```

#### **"Weather/News not working"**
- Check `.env` file exists in project root
- Verify API keys are correct and active
- Check internet connection
- Test API keys directly:
  ```bash
  curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
  ```

## 📱 **Usage Examples**

### **Local Application**
```bash
# Run the desktop application
python main.py

# Expected output:
# =====================================
#     Voice Assistant: Leo
# =====================================
# 
# Commands you can try:
# - "What time is it?"
# - "Tell me a joke"
# - "What's the weather?"
# - "What's the news?"
# - "Open calculator"
# - "Remember to buy milk"
# - "Exit"
# 
# Press Ctrl+C to stop the assistant.
# 
# Listening... (speak now)
```

### **Web Demo**
1. Visit: https://voice-assistant-leo-bte3ynpwrbtf3seehdzhjc.streamlit.app/
2. Click **🎤 Start Voice Command** (allow microphone access)
3. Speak any command
4. Click **🔊 Speak Response** to hear Leo's reply

## 🧪 **Testing**

### **Run Tests**
```bash
# Basic tests
python tests/test_assistant.py

# Test specific functionality
python -c "
from src.commands import CommandHandler
h = CommandHandler()
print('Test 1:', h.handle_command('hello'))
print('Test 2:', h.handle_command('what time is it'))
print('Test 3:', h.handle_command('tell me a joke'))
"
```

### **Verification Script**
```bash
# Complete verification
python -c "
import sys
print('='*60)
print('LEO ASSISTANT VERIFICATION')
print('='*60)
print(f'Python: {sys.version[:6]}')

# Check imports
modules = ['speech_recognition', 'pyttsx3', 'requests', 'dotenv']
for m in modules:
    try:
        __import__(m)
        print(f'✅ {m}')
    except:
        print(f'❌ {m}')

# Check Leo modules
try:
    from src.assistant import VoiceAssistant
    print('✅ Leo Assistant - OK')
except Exception as e:
    print(f'❌ Leo Assistant: {e}')

print('='*60)
"
```

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** and commit: `git commit -m 'Add feature'`
4. **Push**: `git push origin feature/your-feature`
5. **Open Pull Request**

### **Adding New Commands**
Edit `src/commands.py`:
```python
# Add to commands dictionary
self.commands[r'pattern|keywords'] = self.handle_new_command

# Define handler
def handle_new_command(self, text):
    return "Response for new command"
```

### **Reporting Issues**
- **Bug reports**: Include steps to reproduce
- **Feature requests**: Describe use case and benefit
- **Questions**: Ask in GitHub Discussions

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

### **Libraries & APIs Used**
- **[SpeechRecognition](https://github.com/Uberi/speech_recognition)** - Voice recognition
- **[pyttsx3](https://github.com/nateshmbhat/pyttsx3)** - Text-to-speech
- **[streamlit](https://streamlit.io/)** - Web app framework
- **[OpenWeatherMap](https://openweathermap.org/)** - Weather data
- **[NewsAPI](https://newsapi.org/)** - News headlines
- **[Requests](https://github.com/psf/requests)** - HTTP requests

### **Inspiration**
- Inspired by personal assistants like Siri, Alexa, and Google Assistant
- Built for educational purposes and practical utility
- Designed to be lightweight and privacy-focused

## 📞 **Support & Contact**

### **Need Help?**
- **📖 Documentation**: Check this README and [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/Tethi04/voice-assistant-leo/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Tethi04/voice-assistant-leo/discussions)

### **Quick Support Commands**
```bash
# Diagnostic check
python -c "
import sys
print('Python:', sys.version[:6])
import speech_recognition as sr
print('Microphones:', len(sr.Microphone.list_microphone_names()))
import pyttsx3
print('TTS Voices:', len(pyttsx3.init().getProperty('voices')))
"
```

### **Live Demos**
- **🎤 Interactive Voice Demo**: [Streamlit App](https://voice-assistant-leo-bte3ynpwrbtf3seehdzhjc.streamlit.app/)
- **📱 Web Interface**: [GitHub Pages](https://tethi04.github.io/voice-assistant-leo/)
- **💾 Source Code**: [GitHub Repository](https://github.com/Tethi04/voice-assistant-leo)

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=Tethi04/voice-assistant-leo&type=Date)](https://star-history.com/#Tethi04/voice-assistant-leo&Date)

---

<div align="center">

### **Built with ❤️ for the Python Community**

**If Leo helped you, give this repo a star! ⭐**

**Live Demos:**
- 🎤 [Voice Demo](https://voice-assistant-leo-bte3ynpwrbtf3seehdzhjc.streamlit.app/)
- 📱 [Web Demo](https://tethi04.github.io/voice-assistant-leo/)
- 💾 [Source Code](https://github.com/Tethi04/voice-assistant-leo)

[⬆ Back to Top](#-leo---voice-controlled-assistant)

</div>

---

## 📝 **Changelog**

### **v1.0.0** (Initial Release)
- ✅ Basic voice recognition (online/offline)
- ✅ Text-to-speech responses
- ✅ Time, date, jokes, notes
- ✅ Weather and news integration
- ✅ App control and web search
- ✅ Web demos (Streamlit + GitHub Pages)
- ✅ Comprehensive documentation

### **Future Enhancements**
- [ ] Multiple language support
- [ ] Voice customization options
- [ ] Scheduled reminders
- [ ] Email integration
- [ ] Calendar synchronization
- [ ] Smart home device control

---

**Last Updated**: December 2025 
**Maintainer**: [Tethi04](https://github.com/Tethi04)  
**Status**: Actively Maintained

---

*Note: This project is for educational purposes. Always respect privacy and terms of service of APIs used.*
