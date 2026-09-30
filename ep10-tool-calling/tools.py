"""
Episode 10 - tool calling: the model asks, YOUR code runs the function, the model answers.
"""
import json
from datetime import datetime

from llm import MODEL, get_client

client = get_client()


# 1. Plain Python functions: our tools
def multiply(a: float, b: float) -> float:
    return a * b


def current_time() -> str:
    return datetime.now().strftime("%H:%M")


TOOLS = {"multiply": multiply, "current_time": current_time}

# 2. A description of each tool, so the model knows what exists
TOOL_SPECS = [
    {"type": "function", "function": {
        "name": "multiply", "description": "Multiply two numbers exactly.",
        "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"]}}},
    {"type": "function", "function": {
        "name": "current_time", "description": "Get the current local time as HH:MM.",
        "parameters": {"type": "object", "properties": {}}}},
]


def run(question: str) -> None:
    print(f"You: {question}")
    messages = [{"role": "user", "content": question}]
    while True:
        r = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SPECS, temperature=0)
        msg = r.choices[0].message
        if not msg.tool_calls:                      # 5. no more tool requests: this is the answer
            print(f"Bot: {msg.content}\n")
            return
        messages.append(msg)                        # 3. the model asked for a tool
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            result = TOOLS[call.function.name](**args)   # 4. OUR code runs it
            print(f"   [tool] {call.function.name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})


if __name__ == "__main__":
    run("What is 48213 times 7759?")
    run("What is the exact time right now?")
    run("What is the capital of France?")
    print("Correct answer to the first one:", 48213 * 7759)
