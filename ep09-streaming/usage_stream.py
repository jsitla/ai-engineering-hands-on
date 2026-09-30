"""
Episode 9 - streaming AND token counts: ask for usage, and handle the extra last chunk.
"""
from llm import MODEL, get_client

stream = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Name three planets. One line."}],
    temperature=0,
    stream=True,
    stream_options={"include_usage": True},  # <- send token counts at the end
)
for chunk in stream:
    if chunk.choices:  # normal chunks carry text
        print(chunk.choices[0].delta.content or "", end="", flush=True)
    if chunk.usage:    # the very last chunk: no choices, only usage
        print(f"\n\n[last chunk: choices={chunk.choices}, tokens in={chunk.usage.prompt_tokens}, out={chunk.usage.completion_tokens}]")
