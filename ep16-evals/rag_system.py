"""Our RAG assistant from episodes 13-15, with the retrieval method as a setting."""
import math
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from chunkers import by_section
from llm import ask, embed

text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
chunks = by_section(text)
chunk_vectors = embed(chunks)
bm25 = BM25Okapi([re.findall(r"[a-z0-9.]+", c.lower()) for c in chunks])

SYSTEM = """You answer questions about the shop Northwind Home.
Use ONLY the context below. If the answer is not in the context, say: "I don't know, that's not in the handbook."
Keep the answer to one or two sentences."""


def _cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def retrieve(question, method="vector", k=1):
    qv = embed([question])[0]
    by_vector = sorted(range(len(chunks)), key=lambda i: _cos(qv, chunk_vectors[i]), reverse=True)
    if method == "vector":
        ranking = by_vector
    else:  # hybrid: reciprocal rank fusion of vector + BM25
        scores = bm25.get_scores(re.findall(r"[a-z0-9.]+", question.lower()))
        by_bm25 = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)
        fused = {}
        for ranking in (by_vector, by_bm25):
            for pos, i in enumerate(ranking):
                fused[i] = fused.get(i, 0) + 1 / (60 + pos + 1)
        ranking = sorted(fused, key=fused.get, reverse=True)
    return [chunks[i] for i in ranking[:k]]


def answer(question, method="vector", k=1):
    context = "\n\n".join(retrieve(question, method, k))
    return ask(f"Context:\n{context}\n\nQuestion: {question}", system=SYSTEM, temperature=0)
