# src/assistant.py
import speech_recognition as sr
import pyttsx3
import time
import sys
from src.commands import CommandHandler
from src.config import Config

class VoiceAssistant:
    def __init__(self, name="Leo"):
        self.name = name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = self.init_tts()
        self.command_handler = CommandHandler()
        self.is_listening = True
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
    
    def init_tts(self):
        """Initialize text-to-speech engine"""
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        
        # Try to set a natural voice (prefer female voices)
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Set properties
        engine.setProperty('rate', 180)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume 0-1
        
        return engine
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice input"""
        with self.microphone as source:
            print("Listening... (speak now)")
            try:
                audio = self.recognizer.listen(source, timeout=Config.COMMAND_TIMEOUT)
                print("Processing...")
                
                # Try offline recognition first
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    print(f"You (offline): {text}")
                    return text.lower()
                except sr.UnknownValueError:
                    # Fallback to online recognition
                    text = self.recognizer.recognize_google(audio)
                    print(f"You (online): {text}")
                    return text.lower()
                    
            except sr.WaitTimeoutError:
                print("Listening timed out.")
                return ""
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
            except Exception as e:
                print(f"Error in listening: {e}")
                return ""
    
    def process_command(self, command):
        """Process the voice command"""
        if not command:
            return True
        
        response = self.command_handler.handle_command(command)
        
        if response == "exit":
            self.speak("Goodbye! Have a great day.")
            return False
        
        self.speak(response)
        return True
    
    def run(self):
        """Main loop for the assistant"""
        self.speak(f"Hello! I'm {self.name}, your voice assistant. How can I help you today?")
        
        while self.is_listening:
            command = self.listen()
            self.is_listening = self.process_command(command)
            time.sleep(0.5)  # Small delay between commands
    
    def run_once(self):
        """Run assistant for single command (for testing)"""
        command = self.listen()
        return self.process_command(command)
