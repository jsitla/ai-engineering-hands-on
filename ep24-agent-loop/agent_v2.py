"""
Episode 24 - version 2: the same small model, but tools and instructions designed for it.
- one tool returns ALL orders with their details (fewer steps = fewer chances to get lost)
- the system prompt says exactly how to work
"""
from agent import run_agent
from shop_tools import ORDERS, SPECS, add, search_handbook


def get_orders():
    """All orders of the current customer, with date, items, total and shipping in euros."""
    return ORDERS


TOOLS = {"get_orders": get_orders, "add": add, "search_handbook": search_handbook}
SPECS_V2 = [{"type": "function", "function": {"name": "get_orders", "description": get_orders.__doc__,
                                              "parameters": {"type": "object", "properties": {}}}}] + \
           [s for s in SPECS if s["function"]["name"] in ("add", "search_handbook")]
SYSTEM = """You are Nova, the assistant of the shop Northwind Home, helping a logged-in customer.
How to work:
1. For anything about the customer's orders, call get_orders first.
2. To add up amounts, call add with the exact numbers from get_orders.
3. For the shop's rules (delivery, returns, damaged products, payment), call search_handbook.
4. Answer only from tool results. Keep the final answer short, and use euros."""

if __name__ == "__main__":
    run_agent("Which of my orders cost more than 50 euros?", SYSTEM, SPECS_V2, TOOLS)
    run_agent("How much did I pay for shipping in total, across all my orders?", SYSTEM, SPECS_V2, TOOLS)
    run_agent("My vase arrived broken. What should I do?", SYSTEM, SPECS_V2, TOOLS)
