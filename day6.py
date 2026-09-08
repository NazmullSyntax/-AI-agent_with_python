class Agent:

    def __init__(self):
        self.tools = {
            "calculator": self.calculator,
            "greeting": self.greeting
        }

    def calculator(self, a, b):
        return a + b

    def greeting(self):
        return "Hello! I am an AI Agent."

    def decide(self, user_input):

        user_input = user_input.lower()

        if "add" in user_input:
            return "calculator"

        elif "hello" in user_input:
            return "greeting"

        else:
            return None

    def run(self, user_input):

        tool = self.decide(user_input)

        if tool == "calculator":
            return self.tools[tool](10, 20)

        elif tool == "greeting":
            return self.tools[tool]()

        return "I don't know what to do."


agent = Agent()

while True:

    user = input("You: ")

    if user.lower() == "exit":
        break

    result = agent.run(user)

    print("Agent:", result)