"""
Episode 24 - version 3: like version 2, but our code runs only ONE tool call per step.
The small model liked to call get_orders and add at the same time, before it had seen any orders.
"""
from agent import run_agent
from agent_v2 import SPECS_V2, SYSTEM, TOOLS

if __name__ == "__main__":
    for task in ["Which of my orders cost more than 50 euros?",
                 "How much did I pay for shipping in total, across all my orders?",
                 "My vase arrived broken. What should I do?"]:
        run_agent(task, SYSTEM, SPECS_V2, TOOLS, one_at_a_time=True)
