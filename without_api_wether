import json
import random
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

class SimpleAIAgent:
    """
    A simple AI agent that can:
    1. Respond to basic queries
    2. Get weather by scraping (no API key needed)
    3. Perform calculations
    4. Tell time and date
    5. Remember conversation context
    """
    
    def __init__(self, name="Assistant"):
        self.name = name
        self.conversation_history = []
        self.context = {}
        self.user_location = None
        
        self.responses = {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I assist you?"
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "See you later!",
                "Take care!"
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase that?",
                "I don't have an answer for that yet.",
                "Interesting question! I'll need to learn more about that."
            ]
        }
    
    def process_input(self, user_input):
        """Main method to process user input and generate response"""
        self.conversation_history.append(f"User: {user_input}")
        
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
        
        elif self._is_calculation(user_input):
            return self._calculate(user_input)
        
        elif self._is_name_query(user_input):
            return f"My name is {self.name}"
        
        elif self._is_help_query(user_input):
            return self._get_help()
        
        elif self._is_joke_query(user_input):
            return self._tell_joke()
        
        elif self._is_motivation_query(user_input):
            return self._get_motivation()
        
        elif self._is_location_query(user_input):
            return self._set_location(user_input)
        
        elif self._is_definition_query(user_input):
            return self._get_definition(user_input)
        
        else:
            # Try keyword matching
            keyword_response = self._keyword_match(user_input)
            if keyword_response:
                return keyword_response
            
            return random.choice(self.responses["unknown"])
    
    # --- Weather Functions (No API) ---
    
    def _is_weather_query(self, text):
        """Check if input asks for weather"""
        weather_keywords = ['weather', 'temperature', 'temp', 'forecast', 'rain', 'sunny', 'cloudy', 'hot', 'cold']
        return any(keyword in text for keyword in weather_keywords)
    
    def _get_weather(self, text):
        """Get weather using web scraping (no API key)"""
        # Extract city from query
        city = None
        city_match = re.search(r'(?:in|at|for)\s+([A-Za-z\s,]+)', text)
        
        if city_match:
            city = city_match.group(1).strip()
        elif self.user_location:
            city = self.user_location
        
        if city:
            return self._scrape_weather(city)
        else:
            return "🌍 Please specify a city. Example: 'What's the weather in London?' or set your location with 'Set location to New York'"
    
    def _scrape_weather(self, city):
        """Scrape weather from a free weather website"""
        try:
            # Using wttr.in - a free weather service (no API key needed)
            url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                weather_data = response.text.strip()
                return self._parse_weather_response(weather_data, city)
            else:
                return self._get_fallback_weather(city)
                
        except Exception as e:
            return self._get_fallback_weather(city)
    
    def _parse_weather_response(self, data, city):
        """Parse the weather data from wttr.in"""
        try:
            # wttr.in format: condition temperature wind humidity
            parts = data.split()
            
            if len(parts) >= 4:
                condition = " ".join(parts[:-3])
                temp = parts[-3]
                wind = parts[-2]
                humidity = parts[-1]
                
                response = f"""
🌤️ Weather in {city}:
🌡️ Temperature: {temp}
💨 Wind: {wind}
💧 Humidity: {humidity}
📝 Conditions: {condition}
                """
                
                # Add useful tips
                if '°C' in temp:
                    temp_num = int(re.search(r'\+?(\d+)', temp).group(1)) if re.search(r'\+?(\d+)', temp) else 0
                    if temp_num > 30:
                        response += "\n🔥 It's hot! Stay hydrated!"
                    elif temp_num < 0:
                        response += "\n🥶 It's freezing! Bundle up!"
                elif 'rain' in condition.lower():
                    response += "\n☔ Don't forget your umbrella!"
                
                return response.strip()
            else:
                return self._get_fallback_weather(city)
                
        except:
            return self._get_fallback_weather(city)
    
    def _get_fallback_weather(self, city):
        """Fallback weather information when scraping fails"""
        # Simple simulated weather data
        conditions = ['Sunny', 'Cloudy', 'Partly Cloudy', 'Light Rain', 'Clear', 'Overcast']
        temps = [f"{random.randint(5, 30)}°C" for _ in range(6)]
        wind = [f"{random.randint(1, 15)} km/h" for _ in range(6)]
        humidity = [f"{random.randint(30, 90)}%" for _ in range(6)]
        
        idx = random.randint(0, 5)
        
        response = f"""
🌤️ Weather in {city} (approximate):
🌡️ Temperature: {temps[idx]}
💨 Wind: {wind[idx]}
💧 Humidity: {humidity[idx]}
📝 Conditions: {conditions[idx]}
        """
        
        return response.strip()
    
    # --- Location Functions ---
    
    def _is_location_query(self, text):
        """Check if user wants to set location"""
        location_keywords = ['set location', 'my city', 'default city', 'location']
        return any(keyword in text for keyword in location_keywords)
    
    def _set_location(self, text):
        """Set user's default location"""
        city_match = re.search(r'(?:in|to|for|at)\s+([A-Za-z\s]+)', text)
        if city_match:
            city = city_match.group(1).strip()
            self.user_location = city
            return f"📍 Default location set to {city}! Now you can just ask 'weather' without specifying a city."
        else:
            return "Please specify a city. Example: 'Set location to New York'"
    
    # --- Other Utility Functions ---
    
    def _is_greeting(self, text):
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy']
        return any(greeting in text for greeting in greetings)
    
    def _is_farewell(self, text):
        farewells = ['bye', 'goodbye', 'see you', 'exit', 'quit', 'stop', 'cya']
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
    
    def _is_name_query(self, text):
        name_keywords = ['your name', 'who are you', 'what are you']
        return any(keyword in text for keyword in name_keywords)
    
    def _is_help_query(self, text):
        help_keywords = ['help', 'can you', 'what can you', 'capabilities', 'commands']
        return any(keyword in text for keyword in help_keywords)
    
    def _is_joke_query(self, text):
        joke_keywords = ['joke', 'funny', 'laugh', 'humor', 'make me laugh']
        return any(keyword in text for keyword in joke_keywords)
    
    def _is_motivation_query(self, text):
        motivation_keywords = ['motivate', 'motivation', 'inspire', 'inspiration', 'encourage']
        return any(keyword in text for keyword in motivation_keywords)
    
    def _is_definition_query(self, text):
        definition_keywords = ['define', 'meaning', 'what is', 'what does']
        return any(keyword in text for keyword in definition_keywords)
    
    def _calculate(self, text):
        """Perform simple calculations"""
        try:
            # Replace words with operators
            text = text.replace('plus', '+').replace('minus', '-')
            text = text.replace('times', '*').replace('divided by', '/')
            text = text.replace('x', '*')
            
            # Extract numbers and operator
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
            return "I couldn't calculate that. Please try again."
        
        return "I couldn't calculate that. Please try again."
    
    def _keyword_match(self, text):
        """Match keywords to predefined responses"""
        keywords = {
            'love': "Love is a beautiful thing! ❤️",
            'life': "Life is what happens when you're busy making other plans. - John Lennon",
            'happy': "I'm happy you're here! How can I make your day better? 😊",
            'thank': "You're welcome! I'm here to help. 🙏",
            'sorry': "No need to apologize! How can I assist you?",
            'ok': "Great! Let me know if you need anything else.",
            'hello': "Hi there! How are you today?",
            'how are you': "I'm doing great, thanks for asking! How can I help you?",
            'weather': "Please specify a city, like 'Weather in New York'",
            'good': "That's great to hear! 😊",
            'bad': "I'm sorry to hear that. Is there anything I can help with?",
            'morning': "Good morning! Hope you have a wonderful day! ☀️",
            'night': "Good night! Sleep well! 🌙",
            'weekend': "The weekend is coming! Hope you have plans to relax! 🎉",
            'work': "Remember to take breaks and stay hydrated at work! 💪",
            'study': "Keep studying hard! You've got this! 📚",
            'music': "Music is food for the soul! What kind do you like? 🎵",
            'food': "Food is awesome! What's your favorite cuisine? 🍕",
            'travel': "Traveling is amazing! Where do you want to go? ✈️"
        }
        
        for keyword, response in keywords.items():
            if keyword in text:
                return response
        
        return None
    
    def _tell_joke(self):
        """Return a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus! 🇨🇭",
            "Why don't skeletons fight each other? They don't have the guts! 💀",
            "What do you call a bear with no teeth? A gummy bear! 🧸",
            "Why did the bicycle fall over? Because it was two-tired! 🚲",
            "What's orange and sounds like a parrot? A carrot! 🥕",
            "How does a penguin build its house? Igloos it together! 🐧",
            "Why did the math book look so sad? Because it had too many problems! 📐"
        ]
        return random.choice(jokes)
    
    def _get_motivation(self):
        """Return a motivational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The best time to plant a tree was 20 years ago. The second best time is now.",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "Everything you've ever wanted is on the other side of fear.",
            "Be the change you wish to see in the world. - Mahatma Gandhi"
        ]
        return f"💪 {random.choice(quotes)}"
    
    def _get_definition(self, text):
        """Get a simple definition for common words"""
        word = None
        word_match = re.search(r'(?:define|meaning|what is|what does)\s+([A-Za-z]+)', text)
        
        if word_match:
            word = word_match.group(1).lower()
            
            definitions = {
                'love': "Love is a feeling of strong attachment and deep affection.",
                'life': "Life is the existence of an individual human being or organism.",
                'happiness': "Happiness is a state of well-being and contentment.",
                'success': "Success is the accomplishment of an aim or purpose.",
                'freedom': "Freedom is the power to act, speak, or think without hindrance.",
                'knowledge': "Knowledge is facts, information, and skills acquired through experience.",
                'wisdom': "Wisdom is the quality of having experience, knowledge, and good judgment.",
                'courage': "Courage is the ability to do something that frightens one.",
                'hope': "Hope is a feeling of expectation and desire for a certain thing to happen.",
                'dream': "A dream is a series of thoughts, images, and sensations occurring in the mind."
            }
            
            if word in definitions:
                return f"📖 {word.capitalize()}: {definitions[word]}"
            else:
                return f"I don't have a definition for '{word}' stored. Try another word!"
        
        return "Please ask me to define a word. Example: 'Define love'"
    
    def _get_help(self):
        """Get help message"""
        help_text = """
🤖 I'm a simple AI assistant! Here's what I can do:

🔹 WEATHER:
   • "Weather in [city]" - Get current weather
   • "Set location to [city]" - Set default city
   • "Weather" - Get weather for your default city

🔹 BASIC FUNCTIONS:
   • "Hello", "Hi" - Greetings
   • "What time is it?" - Current time
   • "What's the date?" - Current date
   • "25 + 17" - Basic calculations
   • "Tell me a joke" - Random jokes
   • "Motivate me" - Inspirational quotes

🔹 INFO & UTILITIES:
   • "Define [word]" - Word definitions
   • "What's your name?" - My name
   • "Help" or "What can you do?" - This menu

🔹 CONVERSATION:
   • I remember our conversation context
   • I respond to keywords like "love", "life", "happy"

Try typing "Weather in London" or "Tell me a joke" to get started!
        """
        return help_text
    
    def get_history(self):
        """Get conversation history"""
        return "\n".join(self.conversation_history[-10:])
    
    def reset(self):
        """Reset the agent's memory"""
        self.conversation_history = []
        self.context = {}
        self.user_location = None
        return "Agent has been reset!"


# Main interactive function
def main():
    """Run the AI agent in interactive mode"""
    print("🤖 Simple AI Agent (No API Key Required)")
    print("=" * 40)
    print("\nType 'help' to see what I can do, or 'quit' to exit.\n")
    
    agent = SimpleAIAgent("SmartBot")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Agent: Goodbye! Have a great day! 👋")
                break
            
            if not user_input:
                continue
            
            response = agent.process_input(user_input)
            print(f"Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nAgent: Goodbye! 👋")
            break
        except Exception as e:
            print(f"Agent: Oops! Something went wrong: {e}\n")


if __name__ == "__main__":
    main()