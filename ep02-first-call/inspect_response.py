"""
Episode 2 - what actually comes back? Print the whole response object.
"""
from llm import MODEL, get_client

response = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Say hello in three words."}],
)

print("The answer text :", response.choices[0].message.content)
print("Why it stopped  :", response.choices[0].finish_reason)
print("Tokens in       :", response.usage.prompt_tokens)
print("Tokens out      :", response.usage.completion_tokens)
print("Model that ran  :", response.model)
