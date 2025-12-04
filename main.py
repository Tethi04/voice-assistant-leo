# main.py - UPDATED WITH BETTER ERROR HANDLING
import sys
import traceback

def check_dependencies():
    """Check if all required modules are installed"""
    required_modules = [
        'speech_recognition',
        'pyttsx3',
        'python_dotenv',
        'requests',
        'bs4'
    ]
    
    missing = []
    for module in required_modules:
        try:
            if module == 'python_dotenv':
                __import__('dotenv')
            elif module == 'bs4':
                __import__('bs4')
            else:
                __import__(module)
        except ImportError as e:
            missing.append(module)
    
    return missing

def main():
    print("="*50)
    print("        LEO VOICE ASSISTANT")
    print("="*50)
    
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
    
    # Try to import and run
    try:
        from src.assistant import VoiceAssistant
        from src.config import Config
        
        # Validate API keys (just warning, don't stop)
        Config.validate_keys()
        
        # Create and run assistant
        assistant = VoiceAssistant(name=Config.ASSISTANT_NAME)
        
        print(f"\n🎤 Assistant: {assistant.name}")
        print("📋 Available commands:")
        print("   - 'Hello Leo', 'What time is it?', 'Tell me a joke'")
        print("   - 'What's the weather?', 'What's the news?' (needs API keys)")
        print("   - 'Open calculator', 'Remember [note]', 'Exit'")
        print("\n🎯 Speak clearly into your microphone")
        print("   Say 'Exit' to quit")
        print("="*50)
        
        assistant.run()
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n🔧 Try reinstalling dependencies:")
        print("   pip install --upgrade -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()
        print("\n💡 Common solutions:")
        print("   1. Use Python 3.8-3.12 (Python 3.13 has issues)")
        print("   2. Run as Administrator (Windows)")
        print("   3. Check microphone permissions")

if __name__ == "__main__":
    main()
