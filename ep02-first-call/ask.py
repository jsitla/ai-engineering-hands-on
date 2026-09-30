"""
Episode 2 - the same call, but the model comes from your .env file.
Change PROVIDER in .env and this exact code talks to a different AI.

    python ask.py "What is a large language model?"
"""
import sys

from llm import MODEL, PROVIDER, ask

question = " ".join(sys.argv[1:]) or "Explain what an API is in one sentence."
print(f"[{PROVIDER} / {MODEL}]")
print(ask(question))
