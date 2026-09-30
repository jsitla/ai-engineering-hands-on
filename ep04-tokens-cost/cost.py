"""
Episode 4 - what would one answer cost on a paid API?

We run the question on the free local model, read the token counts,
and price the same counts with paid API prices.
Prices are US dollars per 1 million tokens (input, output). They change
often: check the provider's pricing page and update this table.
"""
from llm import MODEL, PROVIDER, get_client

PRICES = {
    "gpt-4.1-mini (OpenAI)": (0.40, 1.60),
    "claude-haiku-4-5 (Anthropic)": (1.00, 5.00),
}

r = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Give me three tips for writing a good email subject line."}],
)
tokens_in, tokens_out = r.usage.prompt_tokens, r.usage.completion_tokens
print(f"[{PROVIDER} / {MODEL}] used {tokens_in} tokens in, {tokens_out} tokens out\n")

print(f"{'Same tokens on':<30} {'1 answer':>12} {'1,000 answers':>15}")
for name, (price_in, price_out) in PRICES.items():
    cost = tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out
    print(f"{name:<30} ${cost:>11.6f} ${cost * 1000:>14.2f}")
