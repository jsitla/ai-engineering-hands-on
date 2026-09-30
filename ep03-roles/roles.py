"""
Episode 3 - the three roles: system, user, assistant.
The model has no memory. It only knows what is in this list.
"""
from llm import MODEL, get_client

client = get_client()

messages = [
    {"role": "system", "content": "You are a friendly assistant. Keep answers short."},
    {"role": "user", "content": "Hi, my name is Maja."},
    {"role": "assistant", "content": "Hi Maja! How can I help you today?"},
    {"role": "user", "content": "What is my name?"},
]

reply = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
print("With the earlier messages   :", reply.choices[0].message.content)

# Now send ONLY the last question
reply = client.chat.completions.create(model=MODEL, messages=messages[-1:], temperature=0)
print("Only the last message       :", reply.choices[0].message.content)
