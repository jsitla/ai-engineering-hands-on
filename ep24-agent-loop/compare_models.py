"""
Episode 24 - how reliable is our agent? Three designs x two small local models, same three tasks.
A task passes when the final answer contains the right facts.
"""
import io
from contextlib import redirect_stdout

import agent
import agent_v2

TASKS = [
    ("Which of my orders cost more than 50 euros?", ["A-1002", "A-1003"], ["A-1001", "A-1004"]),
    ("How much did I pay for shipping in total, across all my orders?", ["48.8"], []),
    ("My vase arrived broken. What should I do?", ["photo"], []),
]
DESIGNS = {
    "v1: list_orders + get_order": (agent.SYSTEM, agent.SPECS, agent.TOOLS, False),
    "v2: get_orders + clear steps": (agent_v2.SYSTEM, agent_v2.SPECS_V2, agent_v2.TOOLS, False),
    "v3: v2 + one tool per step": (agent_v2.SYSTEM, agent_v2.SPECS_V2, agent_v2.TOOLS, True),
}
MODELS = ["llama3.2:3b", "qwen2.5:3b"]

for model in MODELS:
    agent.MODEL = model                      # run_agent reads this module setting
    for design, (system, specs, tools, one) in DESIGNS.items():
        passed = []
        for task, must, must_not in TASKS:
            with redirect_stdout(io.StringIO()):             # hide the step-by-step log
                answer = agent.run_agent(task, system, specs, tools, one) or ""
            ok = all(m in answer for m in must) and not any(m in answer for m in must_not)
            passed.append("PASS" if ok else "fail")
        print(f"{model:<13} {design:<30} {' '.join(passed)}   {passed.count('PASS')}/3")
