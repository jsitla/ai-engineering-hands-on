"""
Episode 26 - the agent gets long-term memory (a small file) and safety limits:
- remember / recall tools, stored in memory.json, so facts survive between conversations
- a step limit, and a stop when it repeats the exact same tool call
"""
import json
from pathlib import Path

import shop_tools
from llm import MODEL, get_client

client = get_client()
MEMORY = Path(__file__).with_name("memory.json")
MAX_STEPS = 8


def remember(fact: str):
    """Save a fact about the customer for future conversations."""
    facts = json.loads(MEMORY.read_text()) if MEMORY.exists() else []
    facts.append(fact)
    MEMORY.write_text(json.dumps(facts, indent=1))
    return "saved"


def recall():
    """All saved facts about the customer."""
    return json.loads(MEMORY.read_text()) if MEMORY.exists() else []


TOOLS = {**shop_tools.TOOLS, "remember": remember, "recall": recall}
SPECS = shop_tools.SPECS + [
    {"type": "function", "function": {"name": "remember", "description": remember.__doc__,
        "parameters": {"type": "object", "properties": {"fact": {"type": "string"}}, "required": ["fact"]}}},
    {"type": "function", "function": {"name": "recall", "description": recall.__doc__, "parameters": {"type": "object", "properties": {}}}},
]
SYSTEM = """You are Nova, the assistant of the shop Northwind Home, helping a logged-in customer.
At the start of every conversation, call recall to see what you know about the customer.
When the customer tells you something useful about themselves, call remember.
Use the other tools to look things up. Give short final answers."""


def run(task, system=None, specs=None, tools=None):
    system, specs, tools = system or SYSTEM, specs or SPECS, tools or TOOLS
    print(f"USER: {task}")
    messages = [{"role": "system", "content": system}, {"role": "user", "content": task}]
    seen = set()
    for step in range(1, MAX_STEPS + 1):
        msg = client.chat.completions.create(model=MODEL, messages=messages, tools=specs, temperature=0).choices[0].message
        if not msg.tool_calls:
            print(f"  step {step}: ANSWER: {msg.content}\n")
            return
        messages.append(msg)
        for call in msg.tool_calls:
            key = (call.function.name, call.function.arguments)
            if key in seen:                                  # same call again = stuck in a loop
                print(f"  step {step}: STOP, repeated call {call.function.name}({call.function.arguments})\n")
                return
            seen.add(key)
            args = json.loads(call.function.arguments or "{}")
            try:
                result = tools[call.function.name](**args)
            except Exception as e:
                result = {"error": str(e)}
            print(f"  step {step}: {call.function.name}({args}) -> {str(result)[:80]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    print(f"  STOP: no answer after {MAX_STEPS} steps\n")


if __name__ == "__main__":
    MEMORY.unlink(missing_ok=True)
    print("=== conversation 1 ===")
    run("Hi! I'm Luka, and I live on the island of Hvar, in Croatia.")
    print("=== conversation 2 (a new chat, empty history) ===")
    run("How long will delivery take to me?")
    print("=== a task it can't do ===")
    run("Please cancel my order A-1003.")
