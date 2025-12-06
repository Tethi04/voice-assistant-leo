# src/commands.py - CORRECTED VERSION
import re
from src.utils import Utils

class CommandHandler:
    def __init__(self):
        self.commands = {
            r'time|what time is it': self.handle_time,
            r'date|what day is it': self.handle_date,
            r'weather|temperature': self.handle_weather,
            r'news|headlines': self.handle_news,
            r'joke|tell me a joke': self.handle_joke,
            r'search|google': self.handle_search,
            r'open (chrome|notepad|calculator)': self.handle_open_app,
            r'note|remember': self.handle_notes,
            r'quit|exit|bye|stop': self.handle_exit,
            r'hello|hi|hey': self.handle_greeting,
            r'your name|who are you': self.handle_introduction
        }
        
        self.notes = []
    
    def handle_command(self, text):
        """Handle voice commands"""
        if not text:
            return "I didn't hear anything. Please try again."
        
        text = text.lower()
        
        for pattern, handler in self.commands.items():
            if re.search(pattern, text):
                return handler(text)
        
        return "Sorry, I didn't understand that command. Try 'time', 'weather', or 'news'."
    
    # FIXED: Added 'self' parameter to all handler methods
    def handle_time(self, text):
        """Handle time command"""
        return f"The current time is {Utils.get_time()}"
    
    def handle_date(self, text):
        """Handle date command"""
        return f"Today is {Utils.get_date()}"
    
    def handle_weather(self, text):
        """Handle weather command"""
        # Extract city from command
        match = re.search(r'weather in (\w+)', text)
        city = match.group(1) if match else "auto"
        return Utils.get_weather(city)
    
    def handle_news(self, text):
        """Handle news command"""
        return Utils.get_news()
    
    def handle_joke(self, text):
        """Handle joke command"""
        return Utils.tell_joke()
    
    def handle_search(self, text):
        """Handle search command"""
        match = re.search(r'search for (.+)', text)
        if match:
            query = match.group(1)
            return Utils.search_web(query)
        return "What would you like me to search for?"
    
    def handle_open_app(self, text):
        """Handle open app command"""
        match = re.search(r'open (\w+)', text)
        if match:
            app = match.group(1)
            return Utils.open_app(app)
        return "Which app would you like to open?"
    
    def handle_notes(self, text):
        """Handle notes command"""
        match = re.search(r'remember (.+)', text)
        if match:
            note = match.group(1)
            self.notes.append(note)
            return f"I'll remember that: {note}"
        
        if 'notes' in text and self.notes:
            notes_text = ", ".join(self.notes)
            return f"Here are your notes: {notes_text}"
        
        return "What would you like me to remember?"
    
    def handle_exit(self, text):
        """Handle exit command"""
        return "exit"
    
    def handle_greeting(self, text):
        """Handle greeting command"""
        import random
        greetings = ["Hello!", "Hi there!", "Hey! How can I help?", "Greetings!"]
        return random.choice(greetings)
    
    def handle_introduction(self, text):
        """Handle introduction command"""
        return "I'm Leo, your voice-controlled assistant. I can help with time, weather, news, jokes, and more!"
