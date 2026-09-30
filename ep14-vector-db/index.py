"""
Episode 14 - store the handbook in a vector database (Chroma), on disk.
Run this once. It embeds every chunk and saves it in the folder ./db
"""
from pathlib import Path

import chromadb

from chunkers import by_section
from llm import embed

text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
chunks = by_section(text)

db = chromadb.PersistentClient(path=str(Path(__file__).parent / "db"))
collection = db.get_or_create_collection("handbook", metadata={"hnsw:space": "cosine"})
collection.upsert(
    ids=[f"chunk-{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embed(chunks),
    metadatas=[{"section": c.split(":", 1)[0]} for c in chunks],
)
print(f"stored {collection.count()} chunks in ./db")
