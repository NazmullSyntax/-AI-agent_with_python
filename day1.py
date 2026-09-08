import json
import random
from datetime import datetime
import re

class SimpleAIAgent:
    """
    A simple AI agent that can:
    1. Respond to basic queries
    2. Remember conversation context
    3. Perform simple calculations
    4. Tell time and date
    5. Use basic NLP for understanding
    """
    
    def __init__(self, name="Assistant"):
        self.name = name
        self.conversation_history = []
        self.context = {}
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
        # Store user input in history
        self.conversation_history.append(f"User: {user_input}")
        
        # Process the input
        response = self._generate_response(user_input)
        
        # Store response in history
        self.conversation_history.append(f"Agent: {response}")
        
        # Keep conversation history manageable
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
        
        elif self._is_calculation(user_input):
            return self._calculate(user_input)
        
        elif self._is_name_query(user_input):
            return f"My name is {self.name}"
        
        elif self._is_weather_query(user_input):
            return self._get_weather_response()
        
        elif self._is_help_query(user_input):
            return self._get_help()
        
        elif self._is_memory_query(user_input):
            return self._handle_memory(user_input)
        
        else:
            # Try to find a keyword match
            keyword_response = self._keyword_match(user_input)
            if keyword_response:
                return keyword_response
            
            return random.choice(self.responses["unknown"])
    
    def _is_greeting(self, text):
        """Check if input is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in text for greeting in greetings)
    
    def _is_farewell(self, text):
        """Check if input is a farewell"""
        farewells = ['bye', 'goodbye', 'see you', 'exit', 'quit', 'stop']
        return any(farewell in text for farewell in farewells)
    
    def _is_time_query(self, text):
        """Check if input asks for time"""
        time_keywords = ['time', 'clock', 'what time', 'current time']
        return any(keyword in text for keyword in time_keywords)
    
    def _is_date_query(self, text):
        """Check if input asks for date"""
        date_keywords = ['date', 'day', 'today', 'what day', 'current date']
        return any(keyword in text for keyword in date_keywords)
    
    def _is_calculation(self, text):
        """Check if input contains a calculation"""
        calc_patterns = [r'\d+\s*[\+\-\*/]\s*\d+', r'\d+\s*plus\s*\d+', r'\d+\s*minus\s*\d+']
        return any(re.search(pattern, text) for pattern in calc_patterns)
    
    def _is_name_query(self, text):
        """Check if input asks for name"""
        name_keywords = ['your name', 'who are you', 'what are you']
        return any(keyword in text for keyword in name_keywords)
    
    def _is_weather_query(self, text):
        """Check if input asks about weather"""
        weather_keywords = ['weather', 'temperature', 'forecast', 'rain']
        return any(keyword in text for keyword in weather_keywords)
    
    def _is_help_query(self, text):
        """Check if input asks for help"""
        help_keywords = ['help', 'can you', 'what can you', 'capabilities']
        return any(keyword in text for keyword in help_keywords)
    
    def _is_memory_query(self, text):
        """Check if input asks about memory/conversation"""
        memory_keywords = ['remember', 'forget', 'recall', 'memory']
        return any(keyword in text for keyword in memory_keywords)
    
    def _calculate(self, text):
        """Perform simple calculations"""
        try:
            # Replace words with operators
            text = text.replace('plus', '+').replace('minus', '-')
            text = text.replace('times', '*').replace('divided by', '/')
            
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
            'weather': "I don't have live weather data, but I recommend checking a weather website!",
            'stock': "I don't track stocks, but you can check financial websites for updates.",
            'news': "I don't have news updates, but you can visit a news website.",
            'joke': "Why don't scientists trust atoms? Because they make up everything!",
            'love': "Love is a beautiful thing! 💖",
            'life': "Life is what happens when you're busy making other plans. - John Lennon",
            'happy': "I'm happy you're here! How can I make your day better?",
            'thank': "You're welcome! I'm here to help.",
            'sorry': "No need to apologize! How can I assist you?",
            'ok': "Great! Let me know if you need anything else."
        }
        
        for keyword, response in keywords.items():
            if keyword in text:
                return response
        
        return None
    
    def _get_weather_response(self):
        """Get weather response"""
        return "I don't have access to real-time weather data. Please check a weather service for accurate information."
    
    def _get_help(self):
        """Get help message"""
        help_text = """
        I'm a simple AI assistant! Here's what I can do:
        ✅ Answer greetings and farewells
        ✅ Tell you the current time and date
        ✅ Perform basic calculations (e.g., 5+3, 10*2)
        ✅ Respond to common questions
        ✅ Remember conversation context
        ✅ Tell jokes
        ✅ Provide motivational quotes
        
        Try asking me things like:
        - "Hello" or "Hi"
        - "What time is it?"
        - "What's 25 + 17?"
        - "Tell me a joke"
        - "What's the date?"
        - "Who are you?"
        """
        return help_text
    
    def _handle_memory(self, text):
        """Handle memory-related queries"""
        if 'remember' in text:
            return "I remember our conversation! You can ask me about previous topics."
        elif 'forget' in text:
            self.conversation_history = []
            return "I've cleared my memory of our conversation."
        else:
            return f"I remember {len(self.conversation_history)} exchanges so far."
    
    def get_history(self):
        """Get conversation history"""
        return "\n".join(self.conversation_history[-10:])  # Show last 10 exchanges
    
    def reset(self):
        """Reset the agent's memory"""
        self.conversation_history = []
        self.context = {}
        return "Agent has been reset!"


# Interactive chatbot function
def main():
    """Run the AI agent in interactive mode"""
    print("🤖 Welcome to Simple AI Agent!")
    print(f"Type 'help' to see what I can do, or 'quit' to exit.\n")
    
    agent = SimpleAIAgent("SmartBot")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"Agent: Goodbye! Have a great day!")
                break
            
            response = agent.process_input(user_input)
            print(f"Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nAgent: Goodbye!")
            break
        except Exception as e:
            print(f"Agent: Oops! Something went wrong: {e}")


if __name__ == "__main__":
    main()