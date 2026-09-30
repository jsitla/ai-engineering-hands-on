"""
Episode 11 - keyword search vs meaning search, on the same FAQ.
"""
import math
import re

from faq import FAQ
from llm import embed


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def keyword_search(query):
    scores = [len(words(query) & words(doc)) for doc in FAQ]
    best = max(range(len(FAQ)), key=lambda i: scores[i])
    return FAQ[best] if scores[best] > 0 else "(no match)"


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


doc_vectors = embed(FAQ)  # embed the FAQ once


def meaning_search(query):
    q = embed([query])[0]
    best = max(range(len(FAQ)), key=lambda i: cosine(q, doc_vectors[i]))
    return FAQ[best]


for query in ["My parcel still hasn't come. How long does it take?",
              "Can I send something back if I don't like it?",
              "When can I phone you?"]:
    print(f"Q: {query}")
    print(f"   keywords: {keyword_search(query)}")
    print(f"   meaning : {meaning_search(query)}\n")
