import unittest
from src.assistant import VoiceAssistant
from src.commands import CommandHandler

class TestVoiceAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = VoiceAssistant(name="TestLeo")
        self.handler = CommandHandler()
    
    def test_time_command(self):
        response = self.handler.handle_command("what time is it")
        self.assertIn("The current time is", response)
    
    def test_date_command(self):
        response = self.handler.handle_command("what date is it")
        self.assertIn("Today is", response)
    
    def test_joke_command(self):
        response = self.handler.handle_command("tell me a joke")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
    
    def test_greeting_command(self):
        response = self.handler.handle_command("hello")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
    
    def test_notes_functionality(self):
        # Test adding a note
        response = self.handler.handle_command("remember buy groceries")
        self.assertIn("I'll remember that", response)
        
        # Test retrieving notes
        response = self.handler.handle_command("show notes")
        self.assertIn("buy groceries", response)

if __name__ == '__main__':
    unittest.main()
