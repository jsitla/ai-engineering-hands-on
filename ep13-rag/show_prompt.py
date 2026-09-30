"""
Episode 13 - what does the model actually receive? Print the full augmented prompt.
"""
from llm import MODEL, get_client
from rag import SYSTEM, retrieve

question = "How much does it cost to deliver a sofa?"
user_message = "Context:\n" + "\n\n".join(retrieve(question)) + f"\n\nQuestion: {question}"
print("=== SYSTEM ===\n" + SYSTEM)
print("\n=== USER ===\n" + user_message)
r = get_client().chat.completions.create(model=MODEL, messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user_message}],
                                         temperature=0, max_tokens=1)
print(f"\n[this prompt is {r.usage.prompt_tokens} tokens]")
