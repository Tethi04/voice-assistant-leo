# main.py - FIXED VERSION
import sys
import traceback
import os

def check_dependencies():
    """Check if all required modules are installed"""
    required_modules = [
        ('speech_recognition', 'SpeechRecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('dotenv', 'python-dotenv'),  # FIXED: 'dotenv' not 'python_dotenv'
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4')     # FIXED: 'bs4' not 'beautifulsoup4'
    ]
    
    missing = []
    for import_name, display_name in required_modules:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            missing.append(display_name)
            print(f"❌ {display_name}")
    
    return missing

def main():
    print("="*50)
    print("        LEO VOICE ASSISTANT")
    print("="*50)
    
    # Check Python version
    print(f"Python version: {sys.version[:6]}")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    missing_modules = check_dependencies()
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("\n📦 Install with:")
        print("   pip install -r requirements.txt")
        print("\n💡 For microphone support:")
        print("   Windows: pip install pipwin && pipwin install pyaudio")
        print("   Mac/Linux: pip install pyaudio")
        return
    
    # Try to import and run
    try:
        from src.assistant import VoiceAssistant
        from src.config import Config
        
        print("\n✅ All modules loaded successfully!")
        
        # Validate API keys
        print("\n🔑 Checking API keys...")
        Config.validate_keys()
        
        # Create and run assistant
        assistant = VoiceAssistant(name=Config.ASSISTANT_NAME)
        
        print(f"\n🎤 Assistant: {assistant.name}")
        print("📋 Available commands:")
        print("   - 'Hello Leo', 'What time is it?', 'Tell me a joke'")
        print("   - 'What's the weather?', 'What's the news?'")
        print("   - 'Open calculator', 'Remember [note]', 'Exit'")
        print("\n🎯 Speak clearly into your microphone")
        print("   Say 'Exit' to quit")
        print("="*50)
        
        assistant.run()
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n🔧 Try:")
        print("   1. Check if src/ folder exists with all .py files")
        print("   2. Run: pip install --upgrade -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        print("\n💡 Common fixes:")
        print("   1. Use Python 3.8-3.11 (not 3.13)")
        print("   2. Run as Administrator (Windows)")
        print("   3. Check microphone permissions")

if __name__ == "__main__":
    main()
