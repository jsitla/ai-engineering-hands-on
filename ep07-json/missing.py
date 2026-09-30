"""
Episode 7 - what happens when the message doesn't contain a field?
A required field forces the model to fill it in. Allowing null lets it say "not given".
"""
import json

from llm import MODEL, get_client

client = get_client()
order = "Hi, please send me 2 blue mugs. Thanks, Ana"   # no city!


def schema(city_type):
    return {
        "type": "object",
        "properties": {
            "customer": {"type": "string"},
            "product": {"type": "string"},
            "quantity": {"type": "integer"},
            "city": {"type": city_type},
        },
        "required": ["customer", "product", "quantity", "city"],
        "additionalProperties": False,
    }


for name, city_type in [("city must be text", "string"), ("city may be null", ["string", "null"])]:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract the order as JSON. Use null for anything the message does not say."},
            {"role": "user", "content": order},
        ],
        response_format={"type": "json_schema", "json_schema": {"name": "order", "schema": schema(city_type), "strict": True}},
        temperature=0,
    )
    print(f"--- {name} ---")
    print(json.loads(r.choices[0].message.content), "\n")
