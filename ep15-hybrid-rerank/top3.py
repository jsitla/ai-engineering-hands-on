"""
Episode 15 - RAG gives the model the top 3 chunks, not just the first.
So: is the answer anywhere in the top 3? And how long does each method take?
"""
import time

from compare import QUESTIONS, bm25_rank, chunks, hybrid_rank, rerank, vector_rank

for name, rank in {"vector search": vector_rank, "BM25 keywords": bm25_rank, "hybrid": hybrid_rank, "hybrid + reranker": rerank}.items():
    start = time.perf_counter()
    hits = sum(any(answer.lower() in chunks[i].lower() for i in rank(q)[:3]) for q, answer in QUESTIONS)
    ms = (time.perf_counter() - start) * 1000 / len(QUESTIONS)
    print(f"{name:<18} answer in top 3: {hits:>2}/{len(QUESTIONS)}   {ms:6.0f} ms per question")
