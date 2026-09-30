"""
Episode 8 - history makes every request bigger. Measure it, then trim it.
"""
from llm import MODEL, get_client

client = get_client()
SYSTEM = {"role": "system", "content": "You are a friendly assistant. Keep answers to one sentence."}
questions = [f"Give me fun fact number {i} about space." for i in range(1, 11)]


def run(max_turns):
    history = []
    sizes = []
    for q in questions:
        history.append({"role": "user", "content": q})
        if max_turns:
            history = history[-max_turns * 2 + 1:]  # keep the last few exchanges + this question
        r = client.chat.completions.create(model=MODEL, messages=[SYSTEM] + history, temperature=0)
        history.append({"role": "assistant", "content": r.choices[0].message.content})
        sizes.append(r.usage.prompt_tokens)
    return sizes


print("tokens sent per turn")
print("keep everything :", run(None))
print("keep last 3     :", run(3))
