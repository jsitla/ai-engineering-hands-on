"""
Episode 10 - what does a tool request from the model actually look like?
"""
from llm import MODEL, get_client
from tools import TOOL_SPECS

r = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What is 48213 times 7759?"}],
    tools=TOOL_SPECS,
    temperature=0,
)
msg = r.choices[0].message
print("content      :", repr(msg.content))
print("finish_reason:", r.choices[0].finish_reason)
for call in msg.tool_calls:
    print("tool call id :", call.id)
    print("function     :", call.function.name)
    print("arguments    :", call.function.arguments, " <- a JSON string, not a dict")
