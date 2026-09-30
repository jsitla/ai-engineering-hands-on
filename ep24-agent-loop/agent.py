"""
Episode 24 - an agent from scratch: the model decides which tools to use, step by step,
until it can answer. Our code runs the tools, and stops the agent after MAX_STEPS.
"""
import json

from llm import MODEL, get_client
from shop_tools import SPECS, TOOLS

client = get_client()
MAX_STEPS = 8
SYSTEM = """You are Nova, the assistant of the shop Northwind Home, helping a logged-in customer.
Use the tools to look things up. Never guess order details or amounts: use get_order and add.
When you have everything you need, give a short final answer."""


def run_agent(task, system=SYSTEM, specs=SPECS, tools=TOOLS, one_at_a_time=False):
    print(f"TASK: {task}")
    messages = [{"role": "system", "content": system}, {"role": "user", "content": task}]
    for step in range(1, MAX_STEPS + 1):
        r = client.chat.completions.create(model=MODEL, messages=messages, tools=specs, temperature=0)
        msg = r.choices[0].message
        if not msg.tool_calls:
            print(f"step {step}: FINAL ANSWER: {msg.content}\n")
            return msg.content
        messages.append(msg)
        for i, call in enumerate(msg.tool_calls):
            args = json.loads(call.function.arguments or "{}")
            if one_at_a_time and i > 0:                 # version 3: run only the first call per step
                result = {"error": "not run: call one tool at a time, and use its result first"}
            else:
                try:
                    result = tools[call.function.name](**args)
                except Exception as e:                  # a bad tool call shouldn't crash the agent
                    result = {"error": str(e)}
            print(f"step {step}: {call.function.name}({args}) -> {str(result)[:90]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    print(f"stopped: no answer after {MAX_STEPS} steps\n")


if __name__ == "__main__":
    run_agent("Which of my orders cost more than 50 euros?")
    run_agent("How much did I pay for shipping in total, across all my orders?")
    run_agent("My vase arrived broken. What should I do?")
