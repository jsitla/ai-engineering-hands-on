"""
Episode 29 - the finished assistant. Instead of one agent that has every tool,
a router sends each message to a small part that does one job well:
  shop rules -> RAG over the handbook (ep 11-15)
  my orders  -> a small agent with two tools, one tool call per step (ep 10, 24)
  about me   -> facts saved to memory (ep 26)
Around it: chat history (ep 8), retries and timeouts (ep 18), guardrails (ep 20), tracing (ep 21).
"""
import json
import math
import re
from pathlib import Path

import shop_tools
from chunkers import by_section
from openai import APIError

from llm import MODEL, embed, get_client
from tracer import save_and_show, span

client = get_client().with_options(max_retries=2, timeout=120)      # ep 18
HERE = Path(__file__).parent
MEMORY = HERE / "memory.json"
MAX_STEPS, MAX_TURNS, MAX_TOKENS = 6, 6, 300                          # MAX_TOKENS: the safety net from ep 22
CHUNKS = by_section(HERE.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8"))
VECTORS = embed(CHUNKS)                                              # once, at start (ep 14, 22)

ROUTER = """Sort the customer's message into exactly one category. Reply as JSON: {"route": "<category>"}.
shop_rules: any question about the shop: delivery, returns, damaged products, payment, gift cards, accounts,
  products, contact details, opening hours.
my_orders: questions about the customer's own orders: what they bought, what they paid, their shipping costs.
about_me: the customer only tells you about themselves (name, where they live), without asking anything.
other: small talk, or anything that has nothing to do with the shop.
Examples:
"How long is a gift card valid?" -> shop_rules
"How much did my last order cost?" -> my_orders
"Hi, I'm Ana and I live in Split." -> about_me"""

RAG_SYSTEM = """You are Nova, the assistant of the shop Northwind Home.
Answer using ONLY the context. If the answer is not in the context, say exactly: "I don't know, the handbook doesn't say."
Use the customer facts when they matter, but never assume anything else about the customer or their order.
One or two short sentences."""

ORDERS_SYSTEM = """You are Nova, the assistant of the shop Northwind Home, helping a logged-in customer with their orders.
Call get_orders first. To add up amounts, call add with the exact numbers from get_orders.
You can NOT cancel or change orders; if asked, point to customer service.
Don't describe your steps: answer with the result only, short, in euros."""

FACTS = """Write the useful facts the customer shares about themselves as JSON: {"facts": ["...", "..."]}.
Only name and where they live. Short phrases, like "name: Ana" or "lives in: Split, Croatia"."""

INJECTION = re.compile(r"ignore (all )?(previous|prior) instructions|note for the ai|you are now|system prompt", re.I)
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?\d{4}){3,}")


def redact(text):                                                    # ep 20
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[email]", text)
    return re.sub(r"\+?\d[\d /-]{7,}\d", "[phone]", text)


def recall():
    return json.loads(MEMORY.read_text()) if MEMORY.exists() else []


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def get_orders():
    """All orders of the current customer, with date, items, total and shipping in euros."""
    return shop_tools.ORDERS


ORDER_TOOLS = {"get_orders": get_orders, "add": shop_tools.add}
ORDER_SPECS = [{"type": "function", "function": {"name": "get_orders", "description": get_orders.__doc__,
                                                 "parameters": {"type": "object", "properties": {}}}}] + \
              [s for s in shop_tools.SPECS if s["function"]["name"] == "add"]


class Nova:
    def __init__(self, show_trace=True):
        self.history = []
        self.show_trace = show_trace

    def chat(self, system, text, **extra):
        messages = [{"role": "system", "content": system}] + self.history + [{"role": "user", "content": text}]
        return client.chat.completions.create(model=MODEL, temperature=0, max_tokens=MAX_TOKENS, messages=messages, **extra)

    def route(self, text):
        with span("route") as s:
            r = client.chat.completions.create(model=MODEL, temperature=0, response_format={"type": "json_object"},
                                               messages=[{"role": "system", "content": ROUTER}, {"role": "user", "content": text}])
            s["route"] = json.loads(r.choices[0].message.content).get("route", "other")
        return s["route"]

    def shop_rules(self, text):
        with span("embed question"):
            q = embed([text])[0]
        with span("retrieve", k=3) as s:
            best = sorted(range(len(CHUNKS)), key=lambda i: cosine(q, VECTORS[i]), reverse=True)[:3]
            chunks = [CHUNKS[i] for i in best if not INJECTION.search(CHUNKS[i])]      # input guard
            s["blocked"] = 3 - len(chunks)
        context = "\n\n".join(chunks)
        facts = "; ".join(recall()) or "none"
        with span("generate") as s:
            r = self.chat(RAG_SYSTEM, f"Customer facts: {facts}\n\nContext:\n{context}\n\nQuestion: {text}")
            s["tokens"] = r.usage.total_tokens
        return r.choices[0].message.content

    def my_orders(self, text):
        messages = [{"role": "system", "content": ORDERS_SYSTEM}] + self.history + [{"role": "user", "content": text}]
        for step in range(1, MAX_STEPS + 1):
            with span(f"model, step {step}"):
                msg = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=MAX_TOKENS,
                                                     messages=messages, tools=ORDER_SPECS).choices[0].message
            if not msg.tool_calls:
                return msg.content
            messages.append(msg)
            for i, call in enumerate(msg.tool_calls):
                if i > 0:                                      # one tool call per step: use the result first
                    result = {"error": "not run: call one tool at a time, and use its result first"}
                else:
                    args = json.loads(call.function.arguments or "{}")
                    with span(f"tool {call.function.name}", args=args):
                        try:
                            result = ORDER_TOOLS[call.function.name](**args)
                        except Exception as e:
                            result = {"error": str(e)}
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        return "Sorry, I couldn't finish that. Please contact customer service."

    def about_me(self, text):
        with span("save facts") as s:
            r = client.chat.completions.create(model=MODEL, temperature=0, response_format={"type": "json_object"},
                                               messages=[{"role": "system", "content": FACTS}, {"role": "user", "content": text}])
            facts = [str(f) for f in json.loads(r.choices[0].message.content).get("facts", [])]
            MEMORY.write_text(json.dumps(recall() + facts, indent=1))
            s["facts"] = facts
        return "Thanks! I'll remember: " + "; ".join(facts) if facts else "Thanks! How can I help?"

    def reply(self, user_text):
        text = redact(user_text)
        try:
            answer = self.answer(text)
        except APIError:                                                                 # ep 18: never show a traceback
            answer = "Sorry, I'm having trouble right now. Please try again in a moment."
        if IBAN.search(answer):                                                          # output guard
            answer = "[blocked by output guard]"
        self.history = (self.history + [{"role": "user", "content": text}, {"role": "assistant", "content": answer}])[-MAX_TURNS * 2:]
        if self.show_trace:
            save_and_show(text[:40])               # the redacted text: no personal data in the log
        return answer

    def answer(self, text):
        route = self.route(text)
        if route == "shop_rules":
            answer = self.shop_rules(text)
        elif route == "my_orders":
            answer = self.my_orders(text)
        elif route == "about_me":
            answer = self.about_me(text)
        else:
            answer = "I don't know, the handbook doesn't say. I can help with your orders and the shop's rules."
        return answer
