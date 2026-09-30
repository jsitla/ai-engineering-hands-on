"""
Episode 7 - turn messy messages into data your code can use.

Attempt 1: just ask for JSON in the prompt.
Attempt 2: JSON mode (the answer must be valid JSON).
Attempt 3: give the model a JSON schema (structured output).
We count how many answers our code can actually read.
"""
import json

from llm import MODEL, get_client
from orders import ORDERS

client = get_client()

SCHEMA = {
    "type": "object",
    "properties": {
        "customer": {"type": "string"},
        "product": {"type": "string"},
        "color": {"type": "string"},
        "quantity": {"type": "integer"},
        "city": {"type": "string"},
    },
    "required": ["customer", "product", "color", "quantity", "city"],
    "additionalProperties": False,
}
FIELDS = set(SCHEMA["required"])


def is_usable(text: str) -> bool:
    """Can our code load it, and does it have every field with the right type?"""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    return (
        isinstance(data, dict)
        and set(data) == FIELDS
        and isinstance(data["quantity"], int)
    )


def run(name: str, **extra) -> None:
    usable = 0
    example = None
    for order in ORDERS:
        r = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Extract the customer, product, color, quantity and city from the order, as JSON."},
                {"role": "user", "content": order},
            ],
            temperature=0,
            **extra,
        )
        text = r.choices[0].message.content
        example = example or text
        usable += is_usable(text)
    print(f"--- {name} ---")
    print(f"First answer: {example.strip()[:200]}")
    print(f"Usable by code: {usable}/{len(ORDERS)}\n")


run("Just asking for JSON")
run("JSON mode", response_format={"type": "json_object"})
run(
    "With a JSON schema",
    response_format={
        "type": "json_schema",
        "json_schema": {"name": "order", "schema": SCHEMA, "strict": True},
    },
)
