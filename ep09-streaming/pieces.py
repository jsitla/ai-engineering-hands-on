"""
Episode 9 - what does one streamed piece look like? Print the first few.
"""
from llm import MODEL, get_client

stream = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Say: streaming works!"}],
    temperature=0,
    stream=True,
)
for i, chunk in enumerate(stream):
    if chunk.choices:
        print(f"piece {i}: {chunk.choices[0].delta.content!r}  finish_reason={chunk.choices[0].finish_reason}")
