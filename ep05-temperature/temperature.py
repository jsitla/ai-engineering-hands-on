"""
Episode 5 - the same prompt five times, at temperature 0 and at 1.
"""
from llm import ask

prompt = "Invent a name for a small coffee shop. Reply with the name only."

for temperature in (0, 1):
    print(f"--- temperature {temperature} ---")
    for _ in range(5):
        print(" ", ask(prompt, temperature=temperature).strip())
    print()
