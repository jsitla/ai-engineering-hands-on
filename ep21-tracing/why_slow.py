"""
Episode 21 - the trace said: embedding ONE question takes over 2 seconds.
But Ollama's own log says each embedding took less than 0.1 seconds. Where does the rest go?
(This test talks to Ollama directly, so run it with PROVIDER=ollama.)
"""
import time

from openai import OpenAI

from llm_v1 import EMBED_MODEL, embed   # the old helper, as it was before this episode's fix

q = ["Is the chat open on Saturday?"]


def timed(label, fn, n=3):
    times = []
    for _ in range(n):
        start = time.perf_counter()
        fn()
        times.append((time.perf_counter() - start) * 1000)
    print(f"{label:<40}" + "".join(f"{t:8.0f} ms" for t in times))


def new_client(host):
    return OpenAI(base_url=f"http://{host}:11434/v1", api_key="ollama")


embed(q)  # make sure the model is loaded
timed("old llm.py embed(): new client each call", lambda: embed(q))
timed("new client, host 'localhost'", lambda: new_client("localhost").embeddings.create(model=EMBED_MODEL, input=q))
timed("new client, host '127.0.0.1'", lambda: new_client("127.0.0.1").embeddings.create(model=EMBED_MODEL, input=q))
client = new_client("localhost")
timed("ONE client, reused, 'localhost'", lambda: client.embeddings.create(model=EMBED_MODEL, input=q))
