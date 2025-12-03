# 🎤 Leo - Voice Controlled Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Offline](https://img.shields.io/badge/Offline-Supported-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)

**A smart voice assistant that works both online and offline**

[Features](#-features) • [Installation](#🚀-installation) • [Usage](#🎯-usage) • [How It Works](#🏗️-how-it-works) • [License](#📄-license)

<img src="https://img.icons8.com/color/96/000000/microphone--v1.png" width="100" alt="Voice Assistant">

</div>

## ✨ Features

### 🟢 **Always Works (Offline)**
- **🎙️ Voice Recognition** - Basic commands work without internet using CMU Sphinx
- **🗣️ Text-to-Speech** - Local speech synthesis using pyttsx3
- **🕒 Time & Date** - Get current time and date
- **😄 Jokes** - Random jokes from a built-in collection
- **📝 Notes** - Remember and recall notes locally
- **🖥️ App Control** - Open calculator, notepad, and other applications
- **🔍 Basic Commands** - Greetings, help, exit commands

### 🌐 **Online Features (Need API Keys)**
- **🌤️ Weather Updates** - Real-time weather for any city worldwide
- **📰 Live News** - Top headlines from global news sources
- **🔍 Web Search** - Google search integration
- **🎤 Enhanced Recognition** - Better speech-to-text with Google's API
- **📍 Auto Location** - Automatic city detection for weather

### 🎯 **Key Highlights**
- **Dual Mode Operation** - Seamlessly switches between offline/online modes
- **Privacy Focused** - Works locally without sending data to cloud
- **Cross-Platform** - Runs on Windows, macOS, and Linux
- **Extensible** - Easy to add new commands and features
- **User-Friendly** - Simple voice commands, no complex syntax required

## 🚀 Installation

### **Prerequisites**
- **Python 3.8 or higher**
- **Microphone** (built-in or external)
- **Speakers** or headphones
- **Internet connection** (for online features only)

### **Step-by-Step Setup**

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/voice-assistant-leo.git
cd voice-assistant-leo
```

#### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install PortAudio (For Microphone)
- **Windows**: Already included with PyAudio
- **macOS**: 
  ```bash
  brew install portaudio
  ```
- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  ```
- **Fedora**:
  ```bash
  sudo dnf install portaudio-devel python3-pyaudio
  ```

#### 5. Configure API Keys (Optional - for online features)
```bash
# 1. Copy the template file
cp config/api_keys.template .env

# 2. Edit .env with your favorite text editor
# 3. Add your API keys (see next section)
```

## 🔑 Getting API Keys (For Online Features)

### **Weather API - OpenWeatherMap**
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" for free account
3. Confirm your email
4. Go to "API Keys" section
5. Copy your default key or create a new one
6. Add to `.env`:
   ```env
   OPENWEATHER_KEY=your_actual_key_here
   ```

### **News API - NewsAPI**
1. Visit [NewsAPI](https://newsapi.org/)
2. Click "Get API Key"
3. Register with your email
4. Verify your email address
5. Copy your API key from dashboard
6. Add to `.env`:
   ```env
   NEWSAPI_KEY=your_actual_key_here
   ```

### **Without API Keys**
If you don't add API keys, Leo will still work with all offline features. You'll see a warning message but can continue using:
- Time/Date
- Jokes
- App control
- Notes
- Basic voice commands

## 🎯 Usage

### **Starting Leo**
```bash
python main.py
```

You'll see this welcome screen:
```
=====================================
    Voice Assistant: Leo
=====================================

Commands you can try:
- "What time is it?"
- "What's the weather?"
- "Tell me a joke"
- "What's the news?"
- "Search for Python tutorials"
- "Open calculator"
- "Remember to buy milk"
- "Exit"

Press Ctrl+C to stop the assistant.
```

Leo will greet you: *"Hello! I'm Leo, your voice assistant. How can I help you today?"*

### **Voice Commands - What You Can Say**

#### **📅 Time & Information**
- "What time is it?"
- "What date is it?"
- "What day is today?"
- "What's the current time?"

#### **😄 Entertainment**
- "Tell me a joke"
- "Say something funny"
- "Make me laugh"

#### **🌤️ Weather** (requires internet + API key)
- "What's the weather?"
- "How's the weather today?"
- "Weather in London"
- "Temperature in New York"
- "Is it raining?"

#### **📰 News** (requires internet + API key)
- "What's the news?"
- "Tell me headlines"
- "Latest news"
- "News update"

#### **🔍 Web & Apps**
- "Search for Python tutorials"
- "Google machine learning"
- "Open calculator"
- "Open notepad"
- "Open Chrome"

#### **💾 Productivity**
- "Remember to buy milk"
- "Note: Meeting at 3 PM"
- "What are my notes?"
- "Show me my reminders"

#### **🛑 Control**
- "Exit"
- "Stop"
- "Goodbye"
- "Quit"
- "Bye Leo"

#### **🎙️ Basic Interaction**
- "Hello Leo"
- "Hi there"
- "How are you?"
- "What can you do?"
- "Help me"
- "Your name"

## 🏗️ How It Works

### **🔧 Technical Architecture**
```
┌─────────────────────────────────────────┐
│           Voice Input                   │
│           (Microphone)                  │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│      Speech Recognition                 │
│  ┌─────────────────────┐                │
│  │   Offline: CMU      │                │
│  │     Sphinx          │                │
│  └─────────────────────┘                │
│  ┌─────────────────────┐                │
│  │   Online: Google    │  ← Fallback    │
│  │    Speech API       │                │
│  └─────────────────────┘                │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│     Command Processing                  │
│  • Pattern Matching                     │
│  • Intent Recognition                   │
│  • Context Handling                     │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│     Service Integration                 │
│  • Local Services (Time, Apps)          │
│  • API Calls (Weather, News)            │
│  • Web Services (Search)                │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│     Text-to-Speech                      │
│  • pyttsx3 (Offline)                    │
│  • Female/Male Voice Selection          │
│  • Speed/Volume Control                 │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│        Voice Output                     │
│        (Speakers)                       │
└─────────────────────────────────────────┘
```

### **📡 Offline vs Online Mode** 

| Feature | Offline Mode | Online Mode | Requirements |
|---------|--------------|-------------|--------------|
| **Speech Recognition** | ✅ CMU Sphinx | ✅ Google Speech API | Internet for online |
| **Text-to-Speech** | ✅ pyttsx3 | ✅ pyttsx3 | None |
| **Time/Date** | ✅ System time | ✅ System time | None |
| **Weather** | ❌ Not available | ✅ OpenWeatherMap API | API Key + Internet |
| **News** | ❌ Not available | ✅ NewsAPI | API Key + Internet |
| **Web Search** | ❌ Not available | ✅ Google Search | Internet |
| **Jokes** | ✅ Local database | ✅ Local database | None |
| **App Control** | ✅ OS commands | ✅ OS commands | None |
| **Notes** | ✅ Local storage | ✅ Local storage | None |

### **🔐 Security & Privacy**
- **No Data Storage**: Your voice commands are processed locally and not stored
- **Optional Online Features**: You control what goes online
- **API Key Protection**: Keys stored in `.env` file (not in code)
- **Local Processing**: Most features work without internet connection
- **Transparent Operation**: You always know when Leo is accessing online services

## 🛠️ Project Structure

### **How GitHub Shows:**
```
voice-assistant-leo/              ← Public Repository
├── .gitignore                    ← Hides sensitive files
├── README.md                     ← This documentation
├── requirements.txt              ← Python dependencies
├── main.py                       ← Main entry point
├── src/                          ← Source code
│   ├── __init__.py
│   ├── assistant.py              ← Main assistant class
│   ├── commands.py               ← Command handlers
│   ├── utils.py                  ← Utility functions
│   └── config.py                 ← Configuration loader
├── config/                       ← Configuration templates
│   └── api_keys.template         ← Template for API keys
├── tests/                        ← Test files
│   └── test_assistant.py         ← Unit tests
└── images/                       ← Screenshots (optional)
```

### **How Your Computer Shows:**
```
voice-assistant-leo/              ← Your local folder
├── .env                          ← YOUR API KEYS (NOT on GitHub!)
├── .gitignore                    ← From GitHub
├── README.md                     ← From GitHub
├── requirements.txt              ← From GitHub
├── main.py                       ← From GitHub
├── src/                          ← From GitHub
│   ├── __init__.py
│   ├── assistant.py
│   ├── commands.py
│   ├── utils.py
│   └── config.py
├── config/
│   └── api_keys.template
├── tests/
│   └── test_assistant.py
├── venv/                         ← Virtual environment (local)
├── __pycache__/                  ← Python cache (local)
└── notes.txt                     ← Your personal notes (auto-created)
```

**Key Difference**: Your computer has `.env` with real API keys, `venv/` folder, and cache files that are NOT uploaded to GitHub.

## 🧪 Testing

### **Run Basic Tests**
```bash
# From project root
python -m pytest tests/

# Or run specific test file
python tests/test_assistant.py
```

### **Test Specific Features**
```bash
# Test offline features
python -c "from src.commands import CommandHandler; h = CommandHandler(); print(h.handle_command('what time is it'))"

# Test joke system
python -c "from src.utils import Utils; print(Utils.tell_joke())"

# Test weather function (requires API key)
python -c "from src.utils import Utils; print(Utils.get_weather('London'))"
```

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### **"Microphone not found"**
**Solution:**
1. Check microphone connection
2. Test microphone in system settings
3. On Windows: Run as Administrator
4. On Linux: Add user to audio group:
   ```bash
   sudo usermod -a -G audio $USER
   ```

#### **"Speech recognition not working"**
**Solution:**
1. Check internet connection (for online mode)
2. Speak clearly and slowly
3. Reduce background noise
4. Adjust microphone sensitivity in system settings
5. Try offline mode: Speak louder and clearer

#### **"Weather/News not working"**
**Solution:**
1. Check if `.env` file exists
2. Verify API keys are correct
3. Check internet connection
4. Test API keys directly:
   ```bash
   curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
   ```

#### **"Text-to-speech not working"**
**Solution:**
1. Check speaker volume
2. Test system sounds
3. On Linux, install espeak:
   ```bash
   sudo apt-get install espeak
   ```
4. On macOS, ensure speech synthesis is enabled

#### **"Module not found errors"**
**Solution:**
```bash
# Reinstall requirements 
pip install --upgrade -r requirements.txt

# Or install missing modules individually
pip install speechrecognition pyttsx3 python-dotenv requests beautifulsoup4
```

#### **"Assistant not responding"**
**Solution:**
1. Check if you're in listening mode (says "Listening...")
2. Wait for the beep/indicator
3. Speak immediately after "Listening..." appears
4. Increase timeout in `src/config.py`:
   ```python
   COMMAND_TIMEOUT = 10  # Increase from 5 to 10 seconds
   ```

## 🚀 Deployment

### **For Personal Use**
1. Clone repository to your computer
2. Create `.env` with your API keys
3. Create desktop shortcut to `main.py`
4. (Optional) Schedule to run at startup

### **For Development**
```bash
# Development setup
git clone https://github.com/YOUR_USERNAME/voice-assistant-leo.git
cd voice-assistant-leo
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if you have dev requirements
```

### **For Production**
1. Use virtual environment
2. Set up proper logging
3. Create startup script
4. Configure as a service:
   - **Windows**: Task Scheduler
   - **Linux**: systemd service
   - **macOS**: launchd

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**: `python -m pytest tests/`
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### **Adding New Commands**
1. Edit `src/commands.py`
2. Add pattern to `self.commands` dictionary
3. Create handler method
4. Add to `src/utils.py` if needed
5. Update README.md documentation
6. Add tests in `tests/test_assistant.py`

### **Reporting Issues**
- Use GitHub Issues
- Include Python version
- Include operating system
- Describe steps to reproduce
- Include error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### **What MIT License Means:**
- ✅ **Free to use** for personal and commercial projects
- ✅ **Freedom to modify** and distribute
- ✅ **Can be used privately**
- ✅ **No warranty** provided
- ✅ **Must include original license** in copies

**You are free to:**
- Use Leo for your internship project
- Modify and improve the code
- Share with classmates
- Use in commercial applications

**You should:**
- Give credit to original authors
- Include the MIT license in distributions
- State significant changes made

## 🙏 Acknowledgments

### **Libraries Used**
- **[SpeechRecognition](https://github.com/Uberi/speech_recognition)** - Speech-to-text functionality
- **[pyttsx3](https://github.com/nateshmbhat/pyttsx3)** - Offline text-to-speech
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[Requests](https://github.com/psf/requests)** - HTTP API calls

### **APIs Used**
- **[OpenWeatherMap](https://openweathermap.org/)** - Weather data
- **[NewsAPI](https://newsapi.org/)** - News headlines
- **[Google Speech API](https://cloud.google.com/speech-to-text)** - Online speech recognition

### **Inspiration**
- Inspired by virtual assistants like Cortana, Siri, and Alexa
- Built for learning Python and AI/ML concepts
- Designed to be accessible for beginners

### **Special Thanks**
- To the open-source community for amazing tools
- To Python developers worldwide
- To internship program mentors and guides

## 📞 Support & Contact

Having trouble with Leo?

**Quick Help:**
1. Check the [Troubleshooting](#🔧-troubleshooting) section
2. Look for similar issues in [GitHub Issues](https://github.com/Tethi04/voice-assistant-leo/issues)
3. Search the error message online

**Need More Help?**
- **Email**: inyunpinky1994@gmail.com
- **GitHub**: [Create an Issue](https://github.com/Tethi04/voice-assistant-leo/issues/new)
- **Documentation**: Read this README thoroughly

**Before asking for help:**
- [ ] Check Python version (`python --version`)
- [ ] Check if microphone is working
- [ ] Test with basic commands
- [ ] Check `.env` file exists (for online features)
- [ ] Try running tests

## 🌟 Star History

If you find this project useful, please consider giving it a star on GitHub! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=Tethi04/voice-assistant-leo&type=Date)](https://star-history.com/#Tethi04/voice-assistant-leo&Date)

---

<div align="center">

**Made with ❤️ by [Tethi Biswas]**

*Part of Python Internship Project Phase*

**Happy Coding! 🚀**

<img src="https://img.icons8.com/color/96/000000/python--v1.png" width="50" alt="Python">
<img src="https://img.icons8.com/color/96/000000/microphone--v1.png" width="50" alt="Microphone">
<img src="https://img.icons8.com/color/96/000000/speech-bubble--v1.png" width="50" alt="Speech">

</div>

---

## 📊 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Core Assistant | ✅ Complete | All basic features working |
| Offline Mode | ✅ Complete | CMU Sphinx integration |
| Online Features | ✅ Complete | Weather, News, Search |
| API Security | ✅ Complete | `.env` protection |
| Documentation | ✅ Complete | This README |
| Testing | ✅ Complete | Unit tests included |
| Cross-Platform | ✅ Complete | Windows, macOS, Linux |

**Last Updated**: December 2025

**Python Version**: 3.8+  
**License**: MIT  
**Maintainer**: [Tethi Biswas]

---

**Note for Internship Submission**: 
- This project demonstrates understanding of Python programming, API integration, voice recognition, and software security
- The `.env` file protection shows awareness of API key security best practices
- Both offline and online modes showcase adaptability and fallback mechanisms
- The modular design allows for easy extension and maintenance
