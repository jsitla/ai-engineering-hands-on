"""
Episode 1 - check that your AI workbench is ready.

Run it from this folder:
    python check_setup.py
Every line should end with OK. If not, the message tells you what to fix.
"""
import json
import sys
import urllib.request

print("Checking your AI workbench...\n")

# 1. Python version
ok_python = sys.version_info >= (3, 10)
print(f"Python {sys.version.split()[0]:<10}", "OK" if ok_python else "-> install Python 3.10 or newer")

# 2. The two libraries we use
for package in ("openai", "dotenv"):
    try:
        __import__(package)
        print(f"Library {package:<9}", "OK")
    except ImportError:
        print(f"Library {package:<9}", "-> run: pip install -r requirements.txt")

# 3. Is Ollama running, and which models does it have?
try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5) as r:
        models = [m["name"] for m in json.load(r)["models"]]
    print("Ollama     ", "OK")
except OSError:
    print("Ollama     ", "-> not running. Start the Ollama app, then try again.")
    sys.exit(1)

from llm import MODEL, PROVIDER, ask

print("Models     ", ", ".join(models) if models else "(none yet)")
if PROVIDER == "ollama" and MODEL not in models:
    print(f"-> run: ollama pull {MODEL}")
    sys.exit(1)

# 4. Ask the model one tiny question
answer = ask("Reply with exactly five words: your workbench is ready.")
print(f"\n{PROVIDER} / {MODEL} says: {answer}")
