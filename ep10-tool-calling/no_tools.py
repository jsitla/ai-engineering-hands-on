"""
Episode 10 - two questions a language model can't answer well on its own.
"""
from llm import ask

for q in ["What is 48213 times 7759? Reply with the number only.", "What is the exact time right now? Reply with the time only."]:
    print(f"You: {q}\nBot: {ask(q, temperature=0)}\n")
print("Correct answer to the first one:", 48213 * 7759)
