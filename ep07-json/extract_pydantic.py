"""
Episode 7 - the same extraction, with the data described as a Python class.
Pydantic builds the JSON schema for us, and checks the values too.
"""
from pydantic import BaseModel, Field

from llm import MODEL, get_client
from orders import ORDERS


class Order(BaseModel):
    customer: str
    product: str = Field(description="the product only, without the color")
    color: str
    quantity: int = Field(gt=0)
    city: str


client = get_client()
for text in ORDERS[:3]:
    r = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract the order."},
            {"role": "user", "content": text},
        ],
        response_format=Order,
        temperature=0,
    )
    order = r.choices[0].message.parsed  # a real Python object, already checked
    print(f"{order.customer:<6} {order.quantity} x {order.color} {order.product} -> {order.city}")
