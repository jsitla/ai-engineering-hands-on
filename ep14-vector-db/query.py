"""
Episode 14 - ask the database. No re-embedding of the handbook: it's already stored.
"""
from pathlib import Path

import chromadb

from llm import embed

db = chromadb.PersistentClient(path=str(Path(__file__).parent / "db"))
collection = db.get_collection("handbook")

question = "Can I pay later?"
result = collection.query(query_embeddings=embed([question]), n_results=3)
print(f"Q: {question}")
for doc, dist in zip(result["documents"][0], result["distances"][0]):
    print(f"  {1 - dist:.2f}  {doc[:90]}...")

# Filter by metadata: only search inside one section
result = collection.query(query_embeddings=embed([question]), n_results=1, where={"section": "Gift cards and discounts"})
print("\nOnly in 'Gift cards and discounts':")
print("  ", result["documents"][0][0][:110], "...")
