"""
Episode 26 - version 2: the same model and loop, with tools and instructions designed for it:
- one get_orders tool instead of list_orders + get_order
- an explicit procedure: when to remember, when to recall
- a clear line about what Nova can NOT do
"""
from memory_agent import MEMORY, SPECS, recall, remember, run
from shop_tools import ORDERS, add, search_handbook


def get_orders():
    """All orders of the current customer, with date, items, total and shipping in euros."""
    return ORDERS


TOOLS = {"get_orders": get_orders, "add": add, "search_handbook": search_handbook, "remember": remember, "recall": recall}
SPECS_V2 = [{"type": "function", "function": {"name": "get_orders", "description": get_orders.__doc__,
                                              "parameters": {"type": "object", "properties": {}}}}] + \
           [s for s in SPECS if s["function"]["name"] in ("add", "search_handbook", "remember", "recall")]
SYSTEM = """You are Nova, the assistant of the shop Northwind Home, helping a logged-in customer.
How to work:
1. When the customer tells you their name or where they live, call remember with that fact.
2. When the answer depends on the customer (for example delivery to them), call recall first.
3. For the customer's orders, call get_orders. For the shop's rules, call search_handbook.
4. You can NOT cancel or change orders. If asked, say so, and point to customer service.
Answer only from tool results. Keep answers short."""

if __name__ == "__main__":
    MEMORY.unlink(missing_ok=True)
    print("=== conversation 1 ===")
    run("Hi! I'm Luka, and I live on the island of Hvar, in Croatia.", SYSTEM, SPECS_V2, TOOLS)
    print("=== conversation 2 (a new chat, empty history) ===")
    run("How long will delivery take to me?", SYSTEM, SPECS_V2, TOOLS)
    print("=== a task it can't do ===")
    run("Please cancel my order A-1003.", SYSTEM, SPECS_V2, TOOLS)
