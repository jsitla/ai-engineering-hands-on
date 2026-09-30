"""
Episode 14 - why a vector database? Speed at scale.
10,000 random vectors stand in for 10,000 chunks (768 numbers each, like our embeddings).
We compare a plain Python loop with Chroma's index.
"""
import random
import time

import chromadb

N, DIM = 10_000, 768
random.seed(1)
vectors = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(N)]
query = [random.gauss(0, 1) for _ in range(DIM)]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb)


start = time.perf_counter()
best_loop = max(range(N), key=lambda i: cosine(query, vectors[i]))
loop_ms = (time.perf_counter() - start) * 1000

db = chromadb.EphemeralClient()
col = db.create_collection("speed", metadata={"hnsw:space": "cosine"})
for i in range(0, N, 1000):  # add in batches
    col.add(ids=[str(j) for j in range(i, i + 1000)], embeddings=vectors[i:i + 1000])
start = time.perf_counter()
best_db = int(col.query(query_embeddings=[query], n_results=1)["ids"][0][0])
db_ms = (time.perf_counter() - start) * 1000

print(f"plain Python loop : {loop_ms:8.1f} ms  best = #{best_loop}, similarity {cosine(query, vectors[best_loop]):.3f}")
print(f"Chroma index      : {db_ms:8.1f} ms  best = #{best_db}, similarity {cosine(query, vectors[best_db]):.3f}")
print(f"same answer: {best_loop == best_db}")
