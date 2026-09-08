import json
import random
from datetime import datetime
import re
import requests
import os

class WeatherAIAgent:
    """
    Enhanced AI agent with real-time weather data integration
    Uses OpenWeatherMap API (free tier)
    """
    
    def __init__(self, name="WeatherBot", api_key=None):
        self.name = name
        self.conversation_history = []
        self.context = {}
        self.user_location = None  # Will store user's city
        self.api_key = api_key or self._get_api_key()
        self.units = "metric"  # Celsius, can change to "imperial" for Fahrenheit
        
        self.responses = {
            "greeting": [
                "Hello! I can tell you the weather anywhere! 🌤️",
                "Hi there! Ask me about the weather in any city!",
                "Greetings! I'm your weather assistant! 🌡️"
            ],
            "farewell": [
                "Goodbye! Stay safe and check the weather! ☂️",
                "See you later! Don't forget your umbrella if needed!",
                "Take care! Let me know if you need weather updates!"
            ],
            "unknown": [
                "I'm not sure about that. Try asking about the weather!",
                "I specialize in weather information. Ask me about any city!",
                "I can help with weather queries. What city are you interested in?"
            ]
        }
    
    def _get_api_key(self):
        """Get API key from environment or prompt user"""
        # Try to get from environment variable first
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        
        if not api_key:
            # Ask user to input their API key
            print("\n🌤️ Weather API Key Required")
            print("Get a free API key at: https://openweathermap.org/api")
            api_key = input("Enter your OpenWeatherMap API key: ").strip()
        
        return api_key
    
    def process_input(self, user_input):
        """Main method to process user input and generate response"""
        self.conversation_history.append(f"User: {user_input}")
        
        # Check if we need to ask for location or set location
        if self._is_set_location(user_input):
            response = self._set_location(user_input)
        else:
            response = self._generate_response(user_input)
        
        self.conversation_history.append(f"Agent: {response}")
        
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    def _generate_response(self, user_input):
        """Generate response based on input analysis"""
        user_input = user_input.lower().strip()
        
        # Check for specific intents
        if self._is_greeting(user_input):
            return random.choice(self.responses["greeting"])
        
        elif self._is_farewell(user_input):
            return random.choice(self.responses["farewell"])
        
        elif self._is_time_query(user_input):
            return f"The current time is {datetime.now().strftime('%I:%M %p')}"
        
        elif self._is_date_query(user_input):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        
        elif self._is_weather_query(user_input):
            return self._get_weather(user_input)
        
        elif self._is_forecast_query(user_input):
            return self._get_forecast(user_input)
        
        elif self._is_comparison_query(user_input):
            return self._compare_weather(user_input)
        
        elif self._is_help_query(user_input):
            return self._get_help()
        
        elif self._is_calculation(user_input):
            return self._calculate(user_input)
        
        else:
            # Check if it's just a city name
            city_match = re.search(r'\b([A-Za-z\s]+)\b', user_input)
            if city_match and len(city_match.group(1).split()) <= 3:
                city = city_match.group(1).strip()
                if len(city) > 2:
                    return self._get_weather_for_city(city)
            
            return random.choice(self.responses["unknown"])
    
    def _is_set_location(self, text):
        """Check if user wants to set a default location"""
        keywords = ['set location', 'default city', 'my city is', 'use city']
        return any(keyword in text.lower() for keyword in keywords)
    
    def _set_location(self, text):
        """Set user's default location"""
        # Extract city name
        city_match = re.search(r'(?:in|to|for|at)\s+([A-Za-z\s]+)', text)
        if city_match:
            city = city_match.group(1).strip()
            self.user_location = city
            return f"📍 Default location set to {city}! Now you can just ask 'weather' without specifying a city."
        else:
            return "Please specify a city. Example: 'Set location to New York'"
    
    def _is_weather_query(self, text):
        """Check if input asks for weather"""
        weather_keywords = ['weather', 'temperature', 'temp', 'forecast', 'rain', 'sunny', 'cloudy']
        return any(keyword in text for keyword in weather_keywords)
    
    def _is_forecast_query(self, text):
        """Check if input asks for forecast"""
        forecast_keywords = ['forecast', 'next week', 'tomorrow', '5 day', 'future']
        return any(keyword in text for keyword in forecast_keywords)
    
    def _is_comparison_query(self, text):
        """Check if user wants to compare weather between cities"""
        compare_keywords = ['compare', 'versus', 'vs', 'difference', 'hotter', 'colder']
        return any(keyword in text for keyword in compare_keywords)
    
    def _get_weather(self, text):
        """Get weather for a city or use default location"""
        # Try to extract city from query
        city = None
        
        # Check for "weather in [city]" pattern
        city_match = re.search(r'(?:in|at|for)\s+([A-Za-z\s,]+)', text)
        if city_match:
            city = city_match.group(1).strip()
        elif self.user_location:
            city = self.user_location
        
        if city:
            return self._get_weather_for_city(city)
        else:
            return "🌍 Please specify a city. Example: 'What's the weather in London?' or set a default location with 'Set location to New York'"
    
    def _get_weather_for_city(self, city):
        """Fetch weather from API for a specific city"""
        if not self.api_key:
            return "⚠️ Weather API key not configured. Please set OPENWEATHER_API_KEY environment variable."
        
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_response(data, city)
            elif response.status_code == 404:
                return f"❌ Could not find weather data for '{city}'. Please check the city name."
            elif response.status_code == 401:
                return "⚠️ Invalid API key. Please check your OpenWeatherMap API key."
            else:
                return f"❌ Error fetching weather data: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Weather service timed out. Please try again later."
        except requests.exceptions.ConnectionError:
            return "🌐 Network error. Please check your internet connection."
        except Exception as e:
            return f"❌ An error occurred: {str(e)}"
    
    def _format_weather_response(self, data, city):
        """Format weather data into a nice response"""
        try:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            city_name = data['name']
            country = data['sys']['country']
            
            # Get temperature unit symbol
            temp_unit = "°C" if self.units == "metric" else "°F"
            wind_unit = "m/s" if self.units == "metric" else "mph"
            
            # Emoji mapping for weather conditions
            weather_icons = {
                'clear': '☀️',
                'clouds': '☁️',
                'rain': '🌧️',
                'drizzle': '🌦️',
                'thunderstorm': '⛈️',
                'snow': '❄️',
                'mist': '🌫️',
                'fog': '🌫️',
                'haze': '🌫️'
            }
            
            # Find appropriate icon
            icon = '🌤️'
            weather_main = data['weather'][0]['main'].lower()
            for key, emoji in weather_icons.items():
                if key in weather_main:
                    icon = emoji
                    break
            
            response = f"""
{icon} Weather in {city_name}, {country}:
🌡️ Temperature: {temp}{temp_unit} (feels like {feels_like}{temp_unit})
🌤️ Conditions: {description.capitalize()}
💧 Humidity: {humidity}%
💨 Wind: {wind_speed} {wind_unit}
            """
            
            # Add some helpful tips
            if temp > 30:
                response += "\n🔥 It's hot! Stay hydrated!"
            elif temp < 0:
                response += "\n🥶 It's freezing! Bundle up!"
            elif 'rain' in description.lower():
                response += "\n☔ Don't forget your umbrella!"
            elif 'snow' in description.lower():
                response += "\n❄️ It's snowing! Drive safely!"
            
            return response.strip()
            
        except KeyError as e:
            return f"⚠️ Error parsing weather data: Missing key {str(e)}"
    
    def _get_forecast(self, text):
        """Get 5-day weather forecast"""
        # Extract city
        city = None
        city_match = re.search(r'(?:in|at|for)\s+([A-Za-z\s,]+)', text)
        if city_match:
            city = city_match.group(1).strip()
        elif self.user_location:
            city = self.user_location
        
        if not city:
            return "Please specify a city for the forecast. Example: 'forecast in Paris'"
        
        if not self.api_key:
            return "⚠️ Weather API key not configured."
        
        try:
            url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units,
                'cnt': 5  # 5 days
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast_response(data, city)
            else:
                return f"❌ Could not get forecast for '{city}'"
                
        except Exception as e:
            return f"❌ Error getting forecast: {str(e)}"
    
    def _format_forecast_response(self, data, city):
        """Format forecast data"""
        forecast_list = data['list'][:5]  # 5 days
        city_name = data['city']['name']
        
        response = f"📅 5-Day Forecast for {city_name}:\n"
        response += "=" * 30 + "\n"
        
        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).strftime('%A')
            temp = item['main']['temp']
            description = item['weather'][0]['description']
            temp_unit = "°C" if self.units == "metric" else "°F"
            
            response += f"{date}: {temp}{temp_unit}, {description.capitalize()}\n"
        
        return response
    
    def _compare_weather(self, text):
        """Compare weather between two cities"""
        cities = re.findall(r'([A-Za-z\s,]+?)(?:\s+vs\s+|\s+and\s+|\s+versus\s+)([A-Za-z\s,]+)', text)
        
        if cities:
            city1, city2 = cities[0]
            city1 = city1.strip()
            city2 = city2.strip()
            
            weather1 = self._get_weather_for_city(city1)
            weather2 = self._get_weather_for_city(city2)
            
            return f"🌍 Weather Comparison:\n\n📍 {city1}:\n{weather1}\n\n📍 {city2}:\n{weather2}"
        else:
            return "To compare weather, say: 'Compare weather in Paris and London'"
    
    def _is_greeting(self, text):
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in text for greeting in greetings)
    
    def _is_farewell(self, text):
        farewells = ['bye', 'goodbye', 'see you', 'exit', 'quit', 'stop']
        return any(farewell in text for farewell in farewells)
    
    def _is_time_query(self, text):
        time_keywords = ['time', 'clock', 'what time', 'current time']
        return any(keyword in text for keyword in time_keywords)
    
    def _is_date_query(self, text):
        date_keywords = ['date', 'day', 'today', 'what day', 'current date']
        return any(keyword in text for keyword in date_keywords)
    
    def _is_calculation(self, text):
        calc_patterns = [r'\d+\s*[\+\-\*/]\s*\d+', r'\d+\s*plus\s*\d+', r'\d+\s*minus\s*\d+']
        return any(re.search(pattern, text) for pattern in calc_patterns)
    
    def _calculate(self, text):
        try:
            text = text.replace('plus', '+').replace('minus', '-')
            text = text.replace('times', '*').replace('divided by', '/')
            
            match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', text)
            if match:
                num1 = float(match.group(1))
                operator = match.group(2)
                num2 = float(match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        return "I can't divide by zero!"
                
                return f"{num1} {operator} {num2} = {result}"
        except:
            return "I couldn't calculate that."
        
        return "I couldn't calculate that."
    
    def _is_help_query(self, text):
        help_keywords = ['help', 'can you', 'what can you', 'capabilities']
        return any(keyword in text for keyword in help_keywords)
    
    def _get_help(self):
        help_text = """
🌤️ WEATHER AI ASSISTANT - HELP

I can help you with weather information worldwide!

COMMANDS:
🔹 "Weather in [city]" - Get current weather
🔹 "Forecast in [city]" - Get 5-day forecast
🔹 "Set location to [city]" - Set default city
🔹 "Weather" (after setting location) - Get default weather
🔹 "Compare [city1] and [city2]" - Compare weather
🔹 "Time" - Current time
🔹 "Date" - Current date
🔹 "[calculation]" - Basic math

EXAMPLES:
• What's the weather in Tokyo?
• Forecast for London
• Set location to Sydney
• Compare Paris and Rome
• What's 25 + 17?

Get your FREE API key at: https://openweathermap.org/api
        """
        return help_text
    
    def get_history(self):
        return "\n".join(self.conversation_history[-10:])
    
    def reset(self):
        self.conversation_history = []
        self.context = {}
        self.user_location = None
        return "Agent has been reset!"


# Interactive function with weather features
def main():
    """Run the weather AI agent"""
    print("🌤️ WEATHER AI AGENT")
    print("=" * 40)
    print("\nFirst, let's set up your weather API key.\n")
    
    agent = WeatherAIAgent()
    
    print("\n🤖 Welcome! I'm your weather assistant!")
    print("Type 'help' to see what I can do, or 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Agent: Goodbye! Stay safe and enjoy the weather! ☀️")
                break
            
            response = agent.process_input(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nAgent: Goodbye! 👋")
            break
        except Exception as e:
            print(f"\nAgent: Oops! Something went wrong: {e}\n")


if __name__ == "__main__":
    main()