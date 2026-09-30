"""
Episode 27 - for comparison: our usual 3B model through Ollama, long prompt + examples.
No fine-tuning at all.
"""
import time

from common import EXAMPLES, LONG_PROMPT, load
from llm import get_client, MODEL

client = get_client()
rows = load("test")
correct, start = 0, time.perf_counter()
messages_before = [{"role": "system", "content": LONG_PROMPT}]
for q, a in EXAMPLES:
    messages_before += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]
for row in rows:
    r = client.chat.completions.create(model=MODEL, temperature=0,
                                       messages=messages_before + [{"role": "user", "content": row["text"]}])
    answer = r.choices[0].message.content.strip().lower().strip(".")
    correct += answer == row["label"]
print(f"bigger model, long prompt + 6 examples: {correct}/{len(rows)}   "
      f"time: {(time.perf_counter() - start) / len(rows):.2f} s per message")
