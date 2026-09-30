"""
Episode 16 - a third version: vector search, but 3 chunks instead of 1.
Same golden set, same scorer.
"""
from cases import CASES
from rag_system import answer

passed = 0
for question, must in CASES:
    reply = answer(question, method="vector", k=3)
    ok = any(m.lower() in reply.lower() for m in must.split("|"))
    passed += ok
    if not ok:
        print(f"   FAIL  {question}\n         -> {reply[:110]}")
print(f"C: vector search, 3 chunks   {passed}/{len(CASES)} passed")
