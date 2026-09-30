"""
Episode 28 - a model that can see: read a receipt image and return structured data.
Needs a vision model:  ollama pull gemma3:4b   (and VISION_MODEL=gemma3:4b, the default here)
"""
import base64
import json
import os
from pathlib import Path

from llm import get_client

VISION_MODEL = os.getenv("VISION_MODEL", "gemma3:4b")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["receipt_no", "date", "items", "total"],
          "properties": {"receipt_no": {"type": "string"}, "date": {"type": "string"}, "total": {"type": "number"},
                         "items": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                   "required": ["quantity", "name", "price"],
                                   "properties": {"quantity": {"type": "integer"}, "name": {"type": "string"}, "price": {"type": "number"}}}}}}



def read(filename):
    image = base64.b64encode(Path(__file__).with_name(filename).read_bytes()).decode()
    r = get_client().chat.completions.create(
        model=VISION_MODEL,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Read this receipt and extract the data as JSON."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image}"}},
        ]}],
        response_format={"type": "json_schema", "json_schema": {"name": "receipt", "schema": SCHEMA, "strict": True}},
        temperature=0,
    )
    data = json.loads(r.choices[0].message.content)
    print(json.dumps(data, indent=1))
    items_sum = round(sum(i["price"] for i in data["items"]), 2)
    print(f"\ncheck: items add up to {items_sum}, receipt total {data['total']} -> {'OK' if items_sum == data['total'] else 'MISMATCH'}")
    return data


if __name__ == "__main__":
    read("receipt.png")
