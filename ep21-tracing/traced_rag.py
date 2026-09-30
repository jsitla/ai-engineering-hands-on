"""
Episode 21 - our RAG assistant with tracing: where does the time go?
"""
import math
from pathlib import Path

from chunkers import by_section
from llm import MODEL, embed, get_client
from tracer import save_and_show, span

client = get_client()
SYSTEM = "You answer questions about the shop Northwind Home. Use ONLY the context. Keep it to one or two sentences."


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def answer(question):
    with span("load handbook"):
        text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
        chunks = by_section(text)
    with span("embed chunks", chunks=len(chunks)):
        vectors = embed(chunks)
    with span("embed question"):
        q = embed([question])[0]
    with span("retrieve", k=3):
        top = sorted(range(len(chunks)), key=lambda i: cosine(q, vectors[i]), reverse=True)[:3]
        context = "\n\n".join(chunks[i] for i in top)
    with span("generate") as s:
        r = client.chat.completions.create(model=MODEL, temperature=0, messages=[
            {"role": "system", "content": SYSTEM}, {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}])
        s["tokens_in"], s["tokens_out"] = r.usage.prompt_tokens, r.usage.completion_tokens
    return r.choices[0].message.content


client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "Hi"}], max_tokens=1)  # warm up
for question in ["How much does it cost to deliver a sofa?", "Is the chat open on Saturday?"]:
    print("answer:", answer(question))
    save_and_show(question)
    print()
