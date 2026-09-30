"""
Episode 18 - a timeout protects you from waiting forever.
We set an unrealistically short timeout to see what happens.
"""
from openai import APITimeoutError, OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama", timeout=0.5, max_retries=0)
try:
    client.chat.completions.create(model="llama3.2:3b", messages=[{"role": "user", "content": "Write a 300 word story."}])
except APITimeoutError as e:
    print("timed out:", type(e).__name__)
    print("-> show the user a friendly message, or try a smaller request")
