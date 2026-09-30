"""
Episode 4 - what does one answer cost?

Prices are in US dollars per 1 million tokens. They change often,
so check your provider's pricing page and update this table.
"""
from llm import MODEL, PROVIDER, get_client

PRICES = {  # model: (input price, output price) per 1M tokens
    "gpt-4.1-mini": (0.40, 1.60),
    "claude-haiku-4-5": (1.00, 5.00),
}

r = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Give me three tips for writing a good email subject line."}],
)
tokens_in, tokens_out = r.usage.prompt_tokens, r.usage.completion_tokens
price_in, price_out = PRICES.get(MODEL, (0.0, 0.0))  # a local model costs nothing per token
cost = tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out

print(f"[{PROVIDER} / {MODEL}]")
print(f"Input tokens : {tokens_in}")
print(f"Output tokens: {tokens_out}")
print(f"This answer  : ${cost:.6f}")
print(f"1,000 answers: ${cost * 1000:.2f}")
