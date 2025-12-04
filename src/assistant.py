# src/assistant.py - UPDATED
import time
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings

class VoiceAssistant:
    def __init__(self, name="Leo"):
        self.name = name
        self.command_handler = self.init_command_handler()
        self.engine = self.init_tts()
        self.is_listening = True
        
        # Initialize speech recognition with error handling
        self.recognizer, self.microphone = self.init_speech_recognition()
    
    def init_speech_recognition(self):
        """Initialize speech recognition with fallback"""
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Adjust for ambient noise
            print("Adjusting for ambient noise...")
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            return recognizer, microphone
        except Exception as e:
            print(f"⚠️  Speech recognition initialization failed: {e}")
            print("   Text input mode will be used instead")
            return None, None
    
    def init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
            return engine
        except Exception as e:
            print(f"⚠️  Text-to-speech initialization failed: {e}")
            return None
    
    def init_command_handler(self):
        """Initialize command handler"""
        try:
            from src.commands import CommandHandler
            return CommandHandler()
        except Exception as e:
            print(f"❌ Command handler failed: {e}")
            return None
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass  # Silent fail if TTS not available
    
    def listen(self):
        """Listen for voice input or use text input"""
        if not self.recognizer or not self.microphone:
            return self.text_input_mode()
        
        try:
            with self.microphone as source:
                print("\n🎤 Listening... (speak now)")
                audio = self.recognizer.listen(source, timeout=5)
                
                # Try offline recognition first
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    print(f"You (offline): {text}")
                    return text.lower()
                except:
                    # Fallback to online recognition
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print(f"You (online): {text}")
                        return text.lower()
                    except:
                        print("Sorry, I didn't catch that")
                        return ""
                        
        except Exception as e:
            print(f"Microphone error: {e}")
            return self.text_input_mode()
    
    def text_input_mode(self):
        """Fallback to text input"""
        print("\n📝 Text Input Mode (microphone not available)")
        print("Type your command and press Enter:")
        return input("You: ").lower()
    
    def process_command(self, command):
        """Process the voice command"""
        if not command or not self.command_handler:
            return True
        
        response = self.command_handler.handle_command(command)
        
        if response == "exit":
            self.speak("Goodbye! Have a great day.")
            return False
        
        self.speak(response)
        return True
    
    def run(self):
        """Main loop for the assistant"""
        self.speak(f"Hello! I'm {self.name}, your voice assistant.")
        
        while self.is_listening:
            command = self.listen()
            self.is_listening = self.process_command(command)
            time.sleep(0.5)
