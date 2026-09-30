"""
Episode 14 - a document changed: update just that chunk, no need to re-embed everything.
"""
from pathlib import Path

import chromadb

from llm import embed

db = chromadb.PersistentClient(path=str(Path(__file__).parent / "db"))
collection = db.get_collection("handbook")
question = "How much does it cost to deliver a sofa?"


def top_answer():
    return collection.query(query_embeddings=embed([question]), n_results=1)["documents"][0][0]


def fee_sentence(text):
    return next(s.strip() for s in text.split(". ") if "flat fee" in s)


hit = collection.query(query_embeddings=embed([question]), n_results=1, include=["documents"])
chunk_id, old_text = hit["ids"][0][0], hit["documents"][0][0]
print("before:", fee_sentence(old_text))

new_text = old_text.replace("flat fee of 39 euros", "flat fee of 45 euros")
collection.upsert(ids=[chunk_id], documents=[new_text], embeddings=embed([new_text]))  # one chunk re-embedded
print("after :", fee_sentence(top_answer()))

collection.upsert(ids=[chunk_id], documents=[old_text], embeddings=embed([old_text]))  # put it back
print(f"(restored; the collection still has {collection.count()} chunks)")
