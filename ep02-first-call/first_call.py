"""
Episode 2 - your first AI call, in about ten lines.
Needs Ollama running with the model pulled (see Episode 1).
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "Explain what an API is in one sentence."}],
)

print(response.choices[0].message.content)
