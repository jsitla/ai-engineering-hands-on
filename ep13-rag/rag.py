"""
Episode 13 - your first RAG: Retrieve the best chunks, Augment the prompt, Generate the answer.
"""
import math
from pathlib import Path

from chunkers import by_section
from llm import ask, embed

# 1. Prepare once: cut the handbook into chunks and embed them
text = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
chunks = by_section(text)
chunk_vectors = embed(chunks)


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


# 2. Retrieve: the k chunks closest in meaning to the question
def retrieve(question, k=3):
    q = embed([question])[0]
    ranked = sorted(range(len(chunks)), key=lambda i: cosine(q, chunk_vectors[i]), reverse=True)
    return [chunks[i] for i in ranked[:k]]


SYSTEM = """You answer questions about the shop Northwind Home.
Use ONLY the context below. If the answer is not in the context, say: "I don't know, that's not in the handbook."
Keep the answer to one or two sentences, and name the section you used in brackets, like [Returns and refunds]."""


# 3. Augment + generate: put the chunks into the prompt
def rag_answer(question):
    context = "\n\n".join(retrieve(question))
    return ask(f"Context:\n{context}\n\nQuestion: {question}", system=SYSTEM, temperature=0)


if __name__ == "__main__":
    for question in ["How much does it cost to deliver a sofa?",
                     "Can I return curtains that were cut to size?",
                     "Do you have a shop in Ljubljana?"]:
        print(f"Q: {question}")
        print(f"   without RAG: {ask(question + ' Answer about the shop Northwind Home in one sentence.', temperature=0)}")
        print(f"   with RAG   : {rag_answer(question)}\n")
