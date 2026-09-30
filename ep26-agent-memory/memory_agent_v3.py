"""
Episode 26 - version 3: memory handled by OUR code, not by the model's choice.
- after every user message, a separate small call pulls out facts worth keeping (JSON)
- before every answer, the saved facts go into the system prompt
The model no longer has to remember to remember.
"""
import json

from llm import MODEL, get_client
from memory_agent import MEMORY, run
from memory_agent_v2 import SPECS_V2, SYSTEM, TOOLS

client = get_client()
FACTS = """Pull out facts about the customer that are worth remembering for future chats: their name, and where they live.
Reply as JSON: {"facts": ["...", "..."]}. If there are none, reply {"facts": []}."""


def save_facts(text):
    r = client.chat.completions.create(model=MODEL, temperature=0, response_format={"type": "json_object"},
                                       messages=[{"role": "system", "content": FACTS}, {"role": "user", "content": text}])
    new = [str(f) for f in json.loads(r.choices[0].message.content).get("facts", [])]
    old = json.loads(MEMORY.read_text()) if MEMORY.exists() else []
    MEMORY.write_text(json.dumps(old + new, indent=1))
    print(f"  [memory] saved: {new}")


def chat(text):
    save_facts(text)                                              # 1. our code saves facts, every time
    facts = json.loads(MEMORY.read_text()) if MEMORY.exists() else []
    system = SYSTEM + "\nWhat you know about the customer: " + ("; ".join(facts) or "nothing yet")   # 2. and loads them
    run(text, system, SPECS_V2, TOOLS)


if __name__ == "__main__":
    MEMORY.unlink(missing_ok=True)
    print("=== conversation 1 ===")
    chat("Hi! I'm Luka, and I live on the island of Hvar, in Croatia.")
    print("=== conversation 2 (a new chat, empty history) ===")
    chat("How long will delivery take to me?")
    print("=== a task it can't do ===")
    chat("Please cancel my order A-1003.")
