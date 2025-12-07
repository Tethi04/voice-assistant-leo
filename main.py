# main.py - CORRECTED VERSION
import sys
import traceback

def check_dependencies():
    """Check if all required modules are installed"""
    required_modules = [
        'speech_recognition',
        'pyttsx3',
        'dotenv',  
        'requests',
        'bs4'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    return missing

def main():
    print("="*60)
    print("            LEO VOICE ASSISTANT")
    print("="*60)
    
    # Check Python version
    print(f"Python version: {sys.version[:6]}")
    
    # Check dependencies
    missing_modules = check_dependencies()
    
    if missing_modules:
        print("\n❌ Missing required modules:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n📦 Install them with:")
        print("   pip install -r requirements.txt")
        print("\n💡 For Windows microphone support, also run:")
        print("   pip install pipwin")
        print("   pipwin install pyaudio")
        return
    
    print("\n✅ All dependencies installed!")
    
    # Try to import and run
    try:
        from src.assistant import VoiceAssistant
        from src.config import Config
        
        # Validate API keys
        Config.validate_keys()
        
        # Create and run assistant
        assistant = VoiceAssistant(name=Config.ASSISTANT_NAME)
        
        print(f"\n🎤 Assistant: {assistant.name}")
        print("📋 Available commands:")
        print("   • 'Hello Leo' - Greeting")
        print("   • 'What time is it?' - Current time")
        print("   • 'Tell me a joke' - Random joke")
        print("   • 'What's the weather?' - Weather info (needs API key)")
        print("   • 'What's the news?' - News headlines (needs API key)")
        print("   • 'Open calculator' - Opens calculator app")
        print("   • 'Remember [note]' - Saves a note")
        print("   • 'What are my notes?' - Shows saved notes")
        print("   • 'Exit' - Close program")
        print("\n🎯 Speak clearly into your microphone")
        print("   Say 'Exit' to quit")
        print("="*60)
        
        assistant.run()
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n🔧 Solutions:")
        print("   1. Check if src/ folder exists with all .py files")
        print("   2. Run: pip install --upgrade -r requirements.txt")
        print("   3. Restart terminal/IDE")
    except KeyboardInterrupt:
        print("\n\n👋 Program stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()
        print("\n💡 Common fixes:")
        print("   1. Run as Administrator (Windows)")
        print("   2. Check microphone permissions")
        print("   3. Use Python 3.8-3.11 (Python 3.12+ may have issues)")
        print("   4. Install PyAudio: pip install pyaudio")

if __name__ == "__main__":
    main()
