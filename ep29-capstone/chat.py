"""
Episode 29 - chat with the finished Nova in the terminal. Type 'quit' to stop.
"""
import sys

from nova import MEMORY, Nova

MEMORY.unlink(missing_ok=True)   # start with an empty memory for the demo
nova = Nova()
while True:
    try:
        text = input("You: ").strip()
    except EOFError:
        break
    if not sys.stdin.isatty():
        print(text)              # show the typed line when input comes from a file
    if text.lower() in ("quit", "exit"):
        break
    if text:
        print("Nova:", nova.reply(text), "\n")
