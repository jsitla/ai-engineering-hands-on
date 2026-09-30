"""
Episode 18 - one request, no retries. If the server has a bad moment, we crash.
Needs flaky_proxy.py running in another terminal.
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11500/v1", api_key="ollama", max_retries=0)
try:
    r = client.chat.completions.create(model="llama3.2:3b", messages=[{"role": "user", "content": "Say hi in three words."}])
    print("answer:", r.choices[0].message.content)
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
