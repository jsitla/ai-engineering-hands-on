"""
Episode 29 - the golden set from episode 16, plus three order tasks, against two versions of Nova:
  one agent with every tool (nova_agent.py), and the router design (nova.py).
A fresh Nova for every question, so earlier answers can't help.
"""
import sys

import nova
import nova_agent
from cases import CASES

AGENT_CASES = [
    ("Which of my orders cost more than 50 euros?", "A-1002&A-1003&!A-1001&!A-1004"),
    ("How much did I pay for shipping in total, across all my orders?", "48.8"),
    ("What did I buy in my most recent order?", "plates"),
]

VERSIONS = [("one agent, every tool", nova_agent), ("router + small parts", nova)]
if "router" in sys.argv:                        # python final_evals.py router  -> test only the router version
    VERSIONS = VERSIONS[1:]
for name, module in VERSIONS:
    module.MEMORY.unlink(missing_ok=True)
    passed, total = 0, 0
    print(f"--- {name} ---")
    for question, must in CASES + AGENT_CASES:
        try:
            reply = module.Nova(show_trace=False).reply(question) or ""
        except Exception as e:                  # the first version has no error handling
            reply = f"ERROR: {type(e).__name__}"
        low = reply.lower()
        if "&" in must:     # all of these, and none of the ones marked with !
            ok = all((m[1:].lower() not in low) if m.startswith("!") else (m.lower() in low) for m in must.split("&"))
        else:
            ok = any(m.lower() in low for m in must.split("|"))
        passed += ok
        total += 1
        if not ok:
            print(f"FAIL  {question}\n      -> {reply[:120]}")
    print(f"{name}: {passed}/{total} passed\n")
