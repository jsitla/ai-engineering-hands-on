"""
Episode 11 - what is an embedding? A long list of numbers that captures meaning.
"""
from llm import EMBED_MODEL, embed

vector = embed(["My puppy loves long walks."])[0]
print(f"model: {EMBED_MODEL}")
print(f"numbers in the list: {len(vector)}")
print("first five:", [round(x, 3) for x in vector[:5]])
