# main.py
from src.assistant import VoiceAssistant
from src.config import Config

def main():
    # Validate API keys
    try:
        Config.validate_keys()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please create a .env file with your API keys.")
        print("Copy config/api_keys.template to .env and add your keys.")
        return
    
    # Create and run assistant
    assistant = VoiceAssistant(name=Config.ASSISTANT_NAME)
    
    print(f"""
    =====================================
        Voice Assistant: {assistant.name}
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
    """)
    
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nAssistant stopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
