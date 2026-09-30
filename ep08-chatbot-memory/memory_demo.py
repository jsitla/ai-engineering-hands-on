"""
Episode 8 - why a chatbot forgets, shown in two runs.
"""
from llm import MODEL, get_client

client = get_client()
SYSTEM = {"role": "system", "content": "You are a friendly assistant. Keep answers to one sentence."}
turns = ["Hi! I'm Luka and I live in Krško.", "I have a dog called Fido.", "What's my name, and what's my dog called?"]


def chat(keep_history: bool) -> None:
    history = [SYSTEM]
    for text in turns:
        history.append({"role": "user", "content": text})
        r = client.chat.completions.create(model=MODEL, messages=history, temperature=0)
        answer = r.choices[0].message.content
        print(f"You: {text}\nBot: {answer}\n")
        if keep_history:
            history.append({"role": "assistant", "content": answer})
        else:
            history = [SYSTEM]  # throw everything away, like a fresh request


print("===== WITHOUT history =====")
chat(keep_history=False)
print("===== WITH history =====")
chat(keep_history=True)
