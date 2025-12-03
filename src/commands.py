# src/commands.py
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
        text = text.lower()
        
        for pattern, handler in self.commands.items():
            if re.search(pattern, text):
                return handler(text)
        
        return "Sorry, I didn't understand that command. Try 'time', 'weather', or 'news'."
    
    def handle_time(self, text):
        return f"The current time is {Utils.get_time()}"
    
    def handle_date(self, text):
        return f"Today is {Utils.get_date()}"
    
    def handle_weather(self, text):
        # Extract city from command
        match = re.search(r'weather in (\w+)', text)
        city = match.group(1) if match else "auto"
        return Utils.get_weather(city)
    
    def handle_news(self, text):
        return Utils.get_news()
    
    def handle_joke(self, text):
        return Utils.tell_joke()
    
    def handle_search(self, text):
        match = re.search(r'search for (.+)', text)
        if match:
            query = match.group(1)
            return Utils.search_web(query)
        return "What would you like me to search for?"
    
    def handle_open_app(self, text):
        match = re.search(r'open (\w+)', text)
        if match:
            app = match.group(1)
            return Utils.open_app(app)
        return "Which app would you like to open?"
    
    def handle_notes(self, text):
        match = re.search(r'remember (.+)', text)
        if match:
            note = match.group(1)
            self.notes.append(note)
            return f"I'll remember that: {note}"
        
        if 'notes' in text and self.notes:
            return "Here are your notes: " + ", ".join(self.notes)
        
        return "What would you like me to remember?"
    
    def handle_exit(self, text):
        return "exit"
    
    def handle_greeting(self, text):
        greetings = ["Hello!", "Hi there!", "Hey! How can I help?", "Greetings!"]
        import random
        return random.choice(greetings)
    
    def handle_introduction(self, text):
        return "I'm Leo, your voice-controlled assistant. I can help with time, weather, news, jokes, and more!"
