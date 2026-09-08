def calculator(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Unknown operation"


def study_agent(user_input):

    user_input = user_input.lower()

    # Decide which tool to use
    if "calculate" in user_input:
        print("Agent: I will use the calculator.")

        result = calculator(10, 20, "multiply")

        return f"The answer is {result}"

    elif "hello" in user_input:
        return "Hello! I am your Study Agent."

    elif "python" in user_input:
        return "Python is a programming language used for many applications."

    else:
        return "Sorry, I don't know how to help."


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Agent: Goodbye!")
        break

    response = study_agent(user_input)

    print("Agent:", response)