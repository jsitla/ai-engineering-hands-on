"""
Episode 11 - similar meaning = similar numbers. Measure it with cosine similarity.
"""
import math

from llm import embed


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


base = "My puppy loves long walks."
others = [
    "My young dog enjoys going for strolls.",   # same meaning, no shared words
    "Dogs need regular exercise.",              # related
    "The invoice is due next Friday.",          # unrelated
]
vectors = embed([base] + others)
print(f"'{base}'\n")
for text, v in zip(others, vectors[1:]):
    print(f"{cosine(vectors[0], v):.2f}  {text}")
