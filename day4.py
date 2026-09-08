import os
from google import genai
from google.genai import types

# 1. Define tools (Python functions the agent can run)
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b

# Map tool names to actual callable functions
TOOLS = {
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers,
}

def main():
    # Initialize the client
    client = genai.Client()

    # User query requiring sequential tool use
    user_prompt = "Add 15 and 27, then multiply the result by 3."
    print(f"User Goal: {user_prompt}\n")

    # Start a chat session with the available tools configured
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[add_numbers, multiply_numbers],
            temperature=0,
        )
    )

    # 2. Agent Execution Loop
    response = chat.send_message(user_prompt)

    while response.function_calls:
        for call in response.function_calls:
            function_name = call.name
            args = call.args

            print(f"[Agent Action] Executing function '{function_name}' with args: {args}")
            
            # Run the tool
            function_to_call = TOOLS[function_name]
            result = function_to_call(**args)
            
            print(f"[Tool Output] Result: {result}\n")

            # Send tool output back to the model so it can plan the next step
            response = chat.send_message(
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result}
                )
            )

    # 3. Final Agent Answer
    print(f"[Final Answer]: {response.text}")

if __name__ == "__main__":
    main()