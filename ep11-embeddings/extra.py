"""
Episode 11 - two more experiments: meaning across languages, and batching.
"""
import math
import time

from faq import FAQ
from llm import embed


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


base, *others = embed(["Where is my parcel?", "Kje je moj paket?", "Where is my package?", "Kje je moja davčna številka?"])
print("'Where is my parcel?' vs")
for text, v in zip(["Kje je moj paket? (Slovenian, same meaning)", "Where is my package? (English, same meaning)", "Kje je moja davčna številka? (Slovenian, 'where is my tax number')"], others):
    print(f"  {cosine(base, v):.2f}  {text}")

start = time.perf_counter()
for sentence in FAQ:
    embed([sentence])            # one request per sentence
one_by_one = time.perf_counter() - start
start = time.perf_counter()
embed(FAQ)                       # one request for all ten
batch = time.perf_counter() - start
print(f"\n10 sentences one by one: {one_by_one:.2f} s   in one batch: {batch:.2f} s")
