"""Tools our agent can use: look up a (made-up) customer's orders, search the handbook, add numbers."""
import math
from pathlib import Path

from chunkers import by_section
from llm import embed

ORDERS = {
    "A-1001": {"date": "2026-08-02", "items": "2 blue mugs", "total": 18.00, "shipping": 4.90},
    "A-1002": {"date": "2026-08-19", "items": "green vase", "total": 64.50, "shipping": 0.00},
    "A-1003": {"date": "2026-09-05", "items": "sofa", "total": 649.00, "shipping": 39.00},
    "A-1004": {"date": "2026-09-21", "items": "4 white plates", "total": 32.00, "shipping": 4.90},
}

_chunks = by_section(Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8"))
_vectors = embed(_chunks)


def list_orders():
    """IDs of all orders of the current customer."""
    return list(ORDERS)


def get_order(order_id: str):
    """Details of one order."""
    return ORDERS.get(order_id, {"error": f"no order {order_id}"})


def add(numbers: list):
    """Add a list of numbers exactly."""
    return round(sum(float(n) for n in numbers), 2)


def search_handbook(question: str):
    """The most relevant handbook paragraph for a question."""
    q = embed([question])[0]
    cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
    return max(zip(_chunks, _vectors), key=lambda cv: cos(q, cv[1]))[0]


TOOLS = {f.__name__: f for f in (list_orders, get_order, add, search_handbook)}
SPECS = [
    {"type": "function", "function": {"name": "list_orders", "description": list_orders.__doc__, "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_order", "description": get_order.__doc__,
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {"name": "add", "description": add.__doc__,
        "parameters": {"type": "object", "properties": {"numbers": {"type": "array", "items": {"type": "number"}}}, "required": ["numbers"]}}},
    {"type": "function", "function": {"name": "search_handbook", "description": search_handbook.__doc__,
        "parameters": {"type": "object", "properties": {"question": {"type": "string"}}, "required": ["question"]}}},
]
