"""
Episode 8 - the trade-off of trimming: what falls out of the list is forgotten.
"""
from llm import MODEL, get_client

client = get_client()
SYSTEM = {"role": "system", "content": "You are a friendly assistant. Keep answers to one sentence."}
turns = ["Hi! My name is Luka."] + [f"Tell me a fun fact about the number {n}." for n in (7, 12, 42, 100)] + ["What is my name?"]


def chat(max_turns):
    history = []
    for text in turns:
        history.append({"role": "user", "content": text})
        if max_turns:
            history = history[-(max_turns * 2 - 1):]
        r = client.chat.completions.create(model=MODEL, messages=[SYSTEM] + history, temperature=0)
        history.append({"role": "assistant", "content": r.choices[0].message.content})
    return history[-1]["content"]


print("keep everything :", chat(None))
print("keep last 3     :", chat(3))
