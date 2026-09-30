"""
Episode 4 - cap the answer length with max_tokens, and see what happens.
"""
from llm import MODEL, get_client

client = get_client()
question = "Give me three tips for writing a good email subject line."

for limit in (None, 40):
    settings = {"max_tokens": limit} if limit else {}
    r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0, **settings)
    print(f"--- max_tokens={limit} ---")
    print(f"tokens out: {r.usage.completion_tokens}, finish_reason: {r.choices[0].finish_reason}")
    print(r.choices[0].message.content.strip()[-160:], "\n")

# The better way: ASK for a short answer
r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": question + " One short line per tip."}], temperature=0)
print("--- asked for short answers ---")
print(f"tokens out: {r.usage.completion_tokens}, finish_reason: {r.choices[0].finish_reason}")
print(r.choices[0].message.content.strip())
