"""
Episode 9 - our chatbot from episode 8, now streaming its answers.
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
    history = history[-(MAX_TURNS * 2 - 1):]

    stream = client.chat.completions.create(model=MODEL, messages=[system] + history, stream=True)
    print("Bot: ", end="", flush=True)
    answer = ""
    for chunk in stream:
        if chunk.choices:
            piece = chunk.choices[0].delta.content or ""
            answer += piece  # collect the pieces, so we can remember the full answer
            print(piece, end="", flush=True)
    print("\n")
    history.append({"role": "assistant", "content": answer})
