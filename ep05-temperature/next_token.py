"""
Episode 5 - look inside: which next tokens did the model consider?
We ask for ONE token and the top 5 candidates with their probabilities.
"""
import math

from llm import MODEL, get_client

prompt = "Complete the sentence with one word. My favourite drink in the morning is"
r = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1,
    logprobs=True,
    top_logprobs=5,
)
print(prompt, "...\n")
for candidate in r.choices[0].logprobs.content[0].top_logprobs:
    p = math.exp(candidate.logprob)
    print(f"{candidate.token!r:>12}  {p:6.1%}  {'#' * round(p * 40)}")

# What temperature does to these chances (using only the top 5, for illustration)
top = {c.token: math.exp(c.logprob) for c in r.choices[0].logprobs.content[0].top_logprobs}
for t in (0.5, 2.0):
    scaled = {k: v ** (1 / t) for k, v in top.items()}
    total = sum(scaled.values())
    print(f"\ntemperature {t}: " + "  ".join(f"{k!r} {v / total:.0%}" for k, v in scaled.items()))
