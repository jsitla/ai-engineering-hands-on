"""
Episode 15 - four ways to find the right chunk, scored on the same 15 questions.
1. vector search (meaning)   2. BM25 (keywords)   3. hybrid (both, fused)   4. hybrid + reranker
"""
import math
import re
from pathlib import Path

from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from chunkers import by_section
from llm import embed
from questions import QUESTIONS

text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
chunks = by_section(text)
chunk_vectors = embed(chunks)


def tokens(t):
    return re.findall(r"[a-z0-9.]+", t.lower())


bm25 = BM25Okapi([tokens(c) for c in chunks])
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def vector_rank(q):
    qv = embed([q])[0]
    return sorted(range(len(chunks)), key=lambda i: cosine(qv, chunk_vectors[i]), reverse=True)


def bm25_rank(q):
    scores = bm25.get_scores(tokens(q))
    return sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)


def hybrid_rank(q, k=60):
    # Reciprocal Rank Fusion: a chunk scores well if it ranks high in EITHER list
    score = {}
    for ranking in (vector_rank(q), bm25_rank(q)):
        for position, i in enumerate(ranking):
            score[i] = score.get(i, 0) + 1 / (k + position + 1)
    return sorted(score, key=score.get, reverse=True)


def rerank(q, top=5):
    candidates = hybrid_rank(q)[:top]
    scores = reranker.predict([(q, chunks[i]) for i in candidates])
    return [i for _, i in sorted(zip(scores, candidates), reverse=True)]


if __name__ == "__main__":
    methods = {"vector search": vector_rank, "BM25 keywords": bm25_rank, "hybrid": hybrid_rank, "hybrid + reranker": rerank}
    for name, rank in methods.items():
        hits = 0
        misses = []
        for q, answer in QUESTIONS:
            if answer.lower() in chunks[rank(q)[0]].lower():
                hits += 1
            else:
                misses.append(q[:38])
        print(f"{name:<18} {hits:>2}/{len(QUESTIONS)}  missed: {misses}")
