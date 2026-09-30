"""
Episode 22 - five ways to make each answer faster and cheaper, measured one at a time.
Every variant answers the same 5 questions; we check the key fact to make sure quality holds.
"""
import json
import math
import time
from pathlib import Path

from chunkers import by_section
from llm import embed, get_client

client = get_client()
HERE = Path(__file__).parent
text = HERE.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
chunks = by_section(text)

QUESTIONS = [("How much does it cost to deliver a sofa?", "39"), ("How long is a gift card valid?", "2 years"),
             ("Is the chat open on Saturday?", "9:00"), ("How long do you keep my invoices?", "10 years"),
             ("How long is the password reset link valid?", "1 hour")]
LONG_SYSTEM = ("You are Nova, a warm and helpful customer assistant for the online shop Northwind Home. "
               "Always greet the customer, thank them for their question, explain the relevant policy in detail, "
               "and offer further help at the end. Use ONLY the context.")
SHORT_SYSTEM = "Answer from the context only, in one short sentence."


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def cached_vectors():
    cache = HERE / "embeddings_cache.json"
    if cache.exists():
        return json.loads(cache.read_text())
    vectors = embed(chunks)
    cache.write_text(json.dumps(vectors))
    return vectors


def run(name, model="llama3.2:3b", system=LONG_SYSTEM, k=3, max_tokens=None, cache=False):
    start = time.perf_counter()
    t_in = t_out = correct = 0
    for question, fact in QUESTIONS:
        vectors = cached_vectors() if cache else embed(chunks)   # re-embedding every time = the slow way
        q = embed([question])[0]
        top = sorted(range(len(chunks)), key=lambda i: cosine(q, vectors[i]), reverse=True)[:k]
        context = "\n\n".join(chunks[i] for i in top)
        extra = {"max_tokens": max_tokens} if max_tokens else {}
        r = client.chat.completions.create(model=model, temperature=0, **extra, messages=[
            {"role": "system", "content": system}, {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}])
        t_in += r.usage.prompt_tokens
        t_out += r.usage.completion_tokens
        correct += fact in r.choices[0].message.content
    seconds = time.perf_counter() - start
    print(f"{name:<34} {t_in:>6} in {t_out:>6} out {seconds:>6.1f} s   correct {correct}/5")


(HERE / "embeddings_cache.json").unlink(missing_ok=True)
client.chat.completions.create(model="llama3.2:3b", messages=[{"role": "user", "content": "Hi"}], max_tokens=1)
run("0. starting point")
run("1. + cache the chunk embeddings", cache=True)
run("2. + only the best chunk (k=1)", cache=True, k=1)
run("3. + short system prompt", cache=True, k=1, system=SHORT_SYSTEM)
run("4. + max_tokens=60 as a safety net", cache=True, k=1, system=SHORT_SYSTEM, max_tokens=60)
client.chat.completions.create(model="llama3.2:1b", messages=[{"role": "user", "content": "Hi"}], max_tokens=1)
run("5. + a smaller model (1B)", model="llama3.2:1b", cache=True, k=1, system=SHORT_SYSTEM, max_tokens=60)
