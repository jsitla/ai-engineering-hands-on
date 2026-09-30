"""
Episode 3 - same question, two different system prompts.
The system message sets the rules before the user says anything.
"""
from llm import ask

question = "I forgot my password. What should I do?"

systems = {
    "Pirate": "You are a pirate. Answer in one short sentence, in pirate speak.",
    "Support desk": (
        "You are the support assistant for an online shop called Northwind. "
        "Answer in at most two sentences. Always tell the user to use the "
        "'Forgot password' link on the login page."
    ),
}

for name, system in systems.items():
    print(f"--- {name} ---")
    print(ask(question, system=system, temperature=0))
    print()
