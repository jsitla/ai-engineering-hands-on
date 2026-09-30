"""
Episode 16 - evals: run the golden set against two versions of our assistant, and score them.
"""
import json
from pathlib import Path

from cases import CASES
from rag_system import answer

VERSIONS = {
    "A: vector search, 1 chunk": dict(method="vector", k=1),
    "B: hybrid search, 3 chunks": dict(method="hybrid", k=3),
}

results = {}
for name, settings in VERSIONS.items():
    passed = 0
    rows = []
    for question, must in CASES:
        reply = answer(question, **settings)
        ok = any(m.lower() in reply.lower() for m in must.split("|"))
        passed += ok
        rows.append({"question": question, "reply": reply, "pass": ok})
    results[name] = rows
    print(f"{name:<28} {passed}/{len(CASES)} passed")
    for r in rows:
        if not r["pass"]:
            print(f"   FAIL  {r['question']}\n         -> {r['reply'][:110]}")

Path(__file__).with_name("results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
