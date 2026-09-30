"""
Episode 10 - one question that needs BOTH tools.
Then: what happens when the model sends the numbers as text, and how to protect your tool.
"""
from tools import TOOLS, run

QUESTION = "What is 12 times 7, and what time is it now?"
try:
    run(QUESTION)
except TypeError as e:
    print(f"CRASH: TypeError: {e}\n")

# The fix: never trust the model's arguments blindly. Convert (and check) them yourself.
TOOLS["multiply"] = lambda a, b: float(a) * float(b)
run(QUESTION)
