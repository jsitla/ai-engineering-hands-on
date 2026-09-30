"""
Episode 8 - a terminal chatbot that remembers.
Type your message and press Enter. Type 'quit' to stop.
"""
from llm import MODEL, PROVIDER, get_client

MAX_TURNS = 10  # keep only the last 10 exchanges, so the history stays small

client = get_client()
system = {"role": "system", "content": "You are a helpful, friendly assistant. Keep answers short."}
history = []

print(f"Chatting with {PROVIDER} / {MODEL}. Type 'quit' to stop.\n")
while True:
    text = input("You: ").strip()
    if text.lower() in {"quit", "exit"}:
        break
    history.append({"role": "user", "content": text})
    history = history[-(MAX_TURNS * 2 - 1):]  # earlier exchanges + your new message

    response = client.chat.completions.create(model=MODEL, messages=[system] + history)
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    print(f"Bot: {answer}\n")
