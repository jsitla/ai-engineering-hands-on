"""
Episode 9 - with streaming: the answer arrives in small pieces while it is written.
"""
import time

from llm import MODEL, get_client

client = get_client()
question = "Explain in about 120 words why the sky is blue."

# warm up: load the model into memory first, so loading time is not measured
client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "Hi"}], max_tokens=1)

start = time.perf_counter()
first = None
pieces = 0
stream = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": question}],
    temperature=0,
    stream=True,  # <- the only change
)
for chunk in stream:
    if not chunk.choices:
        continue
    text = chunk.choices[0].delta.content or ""
    if text and first is None:
        first = time.perf_counter() - start
    pieces += 1
    print(text, end="", flush=True)
total = time.perf_counter() - start
print(f"\n\n[first text after {first:.1f} s, total {total:.1f} s, {pieces} pieces]")
