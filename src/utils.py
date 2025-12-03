# src/utils.py
import datetime
import random
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import sys
import json
from src.config import Config

class Utils:
    @staticmethod
    def get_time():
        """Get current time"""
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")
    
    @staticmethod
    def get_date():
        """Get current date"""
        now = datetime.datetime.now()
        return now.strftime("%B %d, %Y")
    
    @staticmethod
    def get_weather(city="auto"):
        """Get weather information"""
        try:
            if city.lower() == "auto":
                # Get location from IP (simplified)
                response = requests.get("http://ip-api.com/json")
                location_data = response.json()
                city = location_data.get('city', 'London')
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.OPENWEATHER_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                return f"The temperature in {city} is {temp}°C with {description}. Humidity is {humidity}%."
            else:
                return f"Sorry, I couldn't get weather for {city}."
        except Exception as e:
            return f"Error getting weather: {str(e)}"
    
    @staticmethod
    def get_news():
        """Get latest news headlines"""
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={Config.NEWSAPI_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'ok':
                articles = data['articles'][:5]  # Get top 5 articles
                news_text = "Here are the top news headlines:\n"
                for i, article in enumerate(articles, 1):
                    news_text += f"{i}. {article['title']}\n"
                return news_text
            else:
                return "Sorry, I couldn't fetch news at the moment."
        except Exception as e:
            return f"Error getting news: {str(e)}"
    
    @staticmethod
    def tell_joke():
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call fake spaghetti? An impasta!"
        ]
        return random.choice(jokes)
    
    @staticmethod
    def search_web(query):
        """Search the web"""
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"Searching Google for {query}"
    
    @staticmethod
    def open_app(app_name):
        """Open applications based on OS"""
        apps = {
            'chrome': {
                'windows': 'chrome',
                'linux': 'google-chrome',
                'darwin': 'google chrome'
            },
            'notepad': {
                'windows': 'notepad',
                'linux': 'gedit',
                'darwin': 'textedit'
            },
            'calculator': {
                'windows': 'calc',
                'linux': 'gnome-calculator',
                'darwin': 'calculator'
            }
        }
        
        if app_name in apps:
            app_cmd = apps[app_name].get(sys.platform)
            if app_cmd:
                os.system(app_cmd)
                return f"Opening {app_name}"
        
        return f"Sorry, I don't know how to open {app_name}"
