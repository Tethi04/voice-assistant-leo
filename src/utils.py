# src/utils.py - UPDATED WITH PROPER TIMEZONE
import datetime
import random
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import sys
import json
import pytz  # Add this import
from src.config import Config

class Utils:
    @staticmethod
    def get_time():
        """Get current time with timezone support"""
        try:
            # Try to get user's local timezone from browser (for web)
            # For Streamlit Cloud, default to UTC or user's preferred timezone
            # You can change 'Asia/Kolkata' to your timezone
            user_timezone = pytz.timezone('Asia/Kolkata')  # India time
            
            # Get current time in UTC
            utc_now = datetime.datetime.now(pytz.UTC)
            
            # Convert to user's timezone
            local_time = utc_now.astimezone(user_timezone)
            
            return local_time.strftime("%I:%M %p")  # 12-hour format with AM/PM
            
        except:
            # Fallback to server time
            now = datetime.datetime.now()
            return now.strftime("%I:%M %p")
    
    @staticmethod
    def get_date():
        """Get current date with timezone support"""
        try:
            user_timezone = pytz.timezone('Asia/Kolkata')
            utc_now = datetime.datetime.now(pytz.UTC)
            local_date = utc_now.astimezone(user_timezone)
            return local_date.strftime("%B %d, %Y")  # Month Day, Year
        except:
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
            "What do you call fake spaghetti? An impasta!",
            "Why did the computer go to the doctor? It had a virus!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a sleeping dinosaur? A dino-snore!",
            "Why did the tomato turn red? Because it saw the salad dressing!"
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
    
    @staticmethod
    def get_time_with_timezone(timezone='Asia/Kolkata'):
        """Get time for specific timezone"""
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.datetime.now(tz)
            return current_time.strftime("%I:%M %p")
        except:
            return Utils.get_time()
    
    @staticmethod
    def get_detailed_time():
        """Get detailed time information"""
        try:
            user_timezone = pytz.timezone('Asia/Kolkata')
            utc_now = datetime.datetime.now(pytz.UTC)
            local_time = utc_now.astimezone(user_timezone)
            
            return {
                'time_12hr': local_time.strftime("%I:%M %p"),
                'time_24hr': local_time.strftime("%H:%M"),
                'date': local_time.strftime("%B %d, %Y"),
                'day': local_time.strftime("%A"),
                'timezone': str(user_timezone),
                'utc_time': utc_now.strftime("%H:%M UTC")
            }
        except Exception as e:
            now = datetime.datetime.now()
            return {
                'time_12hr': now.strftime("%I:%M %p"),
                'time_24hr': now.strftime("%H:%M"),
                'date': now.strftime("%B %d, %Y"),
                'day': now.strftime("%A"),
                'timezone': 'Local',
                'utc_time': 'N/A'
            }
