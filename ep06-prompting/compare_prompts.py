"""
Episode 6 - a vague prompt vs a clear prompt with examples.
We score both on the same ten messages.
"""
from llm import ask
from messages import LABELS, MESSAGES

VAGUE = "What is this customer message about?"

CLEAR = f"""You sort customer messages for an online shop.
Reply with exactly one word from this list: {", ".join(LABELS)}.
No other text.

Examples:
Message: Where is my order? -> shipping
Message: Why is there an extra fee on my card? -> billing
Message: How do I reset my password? -> account
Message: The lamp flickers when I turn it on. -> product"""


def score(system_prompt: str, name: str) -> None:
    correct = 0
    print(f"--- {name} ---")
    for text, expected in MESSAGES:
        answer = ask(f"Message: {text}", system=system_prompt, temperature=0).strip()
        hit = answer.lower().strip(".") == expected
        correct += hit
        print(f"{'OK ' if hit else 'X  '} {answer[:60]!r}")
    print(f"Score: {correct}/{len(MESSAGES)}\n")


score(VAGUE, "Vague prompt")
score(CLEAR, "Clear prompt + examples")
