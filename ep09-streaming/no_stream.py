"""
Episode 9 - without streaming: you wait for the WHOLE answer, then see it at once.
"""
import time

from llm import MODEL, get_client

client = get_client()
question = "Explain in about 120 words why the sky is blue."

# warm up: load the model into memory first, so loading time is not measured
client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "Hi"}], max_tokens=1)

start = time.perf_counter()
r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0)
waited = time.perf_counter() - start
print(r.choices[0].message.content)
print(f"\n[first text after {waited:.1f} s, total {waited:.1f} s]")
