"""
Episode 19 - prompt caching, measured on a local model.
When a new request starts with EXACTLY the same text as the previous one,
the server can reuse the work it already did on that part (the "prefix").
"""
import time
from pathlib import Path

from llm import MODEL, get_client

client = get_client()
handbook = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
SYSTEM = "You answer questions about the shop Northwind Home, using only this handbook.\n\n" + handbook


def ask_timed(system, question):
    start = time.perf_counter()
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": question}],
        temperature=0,
        max_tokens=20,  # short answers, so we mostly measure reading the prompt
    )
    return time.perf_counter() - start, r.usage.prompt_tokens


client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "Hi"}], max_tokens=1)  # load the model

runs = [
    ("1. first time with the handbook", SYSTEM, "How much does it cost to deliver a sofa?"),
    ("2. same handbook, new question", SYSTEM, "How long is a gift card valid?"),
    ("3. same handbook, new question", SYSTEM, "Is the chat open on Saturday?"),
    ("4. one word changed at the START", SYSTEM.replace("You answer", "You kindly answer"), "Is the chat open on Saturday?"),
]
for name, system, question in runs:
    seconds, tokens = ask_timed(system, question)
    print(f"{name:<36} {tokens:>5} prompt tokens   {seconds:5.2f} s")
