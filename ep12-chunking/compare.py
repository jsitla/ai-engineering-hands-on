"""
Episode 12 - same document, same questions, three chunking strategies.
For each question we take the ONE best-matching chunk and check if it contains the answer.
"""
import math
from pathlib import Path

from chunkers import by_section, fixed, fixed_overlap
from llm import embed
from questions import QUESTIONS

text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


question_vectors = embed([q for q, _ in QUESTIONS])

for name, chunker in [("fixed 300 characters", fixed), ("fixed 300 + 100 overlap", fixed_overlap), ("by section", by_section)]:
    chunks = chunker(text)
    vectors = embed(chunks)
    hits = 0
    for (question, answer), qv in zip(QUESTIONS, question_vectors):
        best = max(range(len(chunks)), key=lambda i: cosine(qv, vectors[i]))
        hits += answer.lower() in chunks[best].lower()
    print(f"{name:<25} {len(chunks):>3} chunks   answer found {hits}/{len(QUESTIONS)}")

print("\nExample of a fixed-size chunk:")
print(repr(fixed(text)[3]))
