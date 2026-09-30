"""
Episode 12 - does chunk size matter? Fixed-size chunks (with overlap) at four sizes.
"""
import math
from pathlib import Path

from chunkers import fixed_overlap
from llm import embed
from questions import QUESTIONS

text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
question_vectors = embed([q for q, _ in QUESTIONS])


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


for size in (150, 300, 600, 1200):
    chunks = fixed_overlap(text, size=size, overlap=size // 3)
    vectors = embed(chunks)
    hits = sum(answer.lower() in chunks[max(range(len(chunks)), key=lambda i: cosine(qv, vectors[i]))].lower()
               for (_, answer), qv in zip(QUESTIONS, question_vectors))
    print(f"size {size:>5} characters  {len(chunks):>3} chunks   answer found {hits}/{len(QUESTIONS)}")
