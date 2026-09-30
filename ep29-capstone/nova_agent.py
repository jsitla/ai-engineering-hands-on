"""
Episode 29 - first try: ONE agent that has every tool. (Compare with nova.py.)
  chat history (ep 8) + tools and an agent loop (ep 10, 24) + handbook search (ep 11-15)
  + memory (ep 26) + retries and timeouts (ep 18) + guardrails (ep 20) + tracing (ep 21)
"""
import json
import re
from pathlib import Path

import shop_tools
from llm import MODEL, get_client
from tracer import save_and_show, span

client = get_client().with_options(max_retries=4, timeout=60)      # ep 18
MAX_STEPS, MAX_TURNS = 8, 6                                          # ep 26, ep 8
MEMORY = Path(__file__).with_name("memory.json")

SYSTEM = """You are Nova, the assistant of the shop Northwind Home, helping a logged-in customer.
How to work:
1. For anything about the customer's orders, call get_orders first.
2. To add up amounts, call add with the exact numbers from get_orders.
3. For the shop's rules (delivery, returns, damaged products, payment, gift cards, account), call search_handbook,
   and answer ONLY from what it returns. If it doesn't say, answer: "I don't know, the handbook doesn't say."
4. When the customer tells you something useful about themselves (name, where they live), call remember.
   Call recall when their details could change the answer.
Give short, friendly final answers, in euros."""


# --- memory tools (ep 26)
def remember(fact: str):
    """Save a fact about the customer for future conversations."""
    facts = json.loads(MEMORY.read_text()) if MEMORY.exists() else []
    MEMORY.write_text(json.dumps(facts + [fact], indent=1))
    return "saved"


def recall():
    """All saved facts about the customer."""
    return json.loads(MEMORY.read_text()) if MEMORY.exists() else []


def get_orders():
    """All orders of the current customer, with date, items, total and shipping in euros."""
    return shop_tools.ORDERS


# fewer, bigger tools work better with small models (ep 24)
TOOLS = {"get_orders": get_orders, "add": shop_tools.add, "search_handbook": shop_tools.search_handbook,
         "remember": remember, "recall": recall}
SPECS = [{"type": "function", "function": {"name": "get_orders", "description": get_orders.__doc__,
                                           "parameters": {"type": "object", "properties": {}}}}] + \
        [s for s in shop_tools.SPECS if s["function"]["name"] in ("add", "search_handbook")] + [
    {"type": "function", "function": {"name": "remember", "description": remember.__doc__,
        "parameters": {"type": "object", "properties": {"fact": {"type": "string"}}, "required": ["fact"]}}},
    {"type": "function", "function": {"name": "recall", "description": recall.__doc__, "parameters": {"type": "object", "properties": {}}}},
]

# --- guardrails (ep 20)
INJECTION = re.compile(r"ignore (all )?(previous|prior) instructions|note for the ai|you are now|system prompt", re.I)
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?\d{4}){3,}")


def redact(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[email]", text)
    return re.sub(r"\+?\d[\d /-]{7,}\d", "[phone]", text)


def run_tool(name, args):
    try:
        result = TOOLS[name](**args)
    except Exception as e:                                   # a bad tool call shouldn't crash Nova
        result = {"error": str(e)}
    if name == "search_handbook" and INJECTION.search(str(result)):
        result = {"error": "blocked: this text contained instructions for the AI"}
    return result


class Nova:
    def __init__(self, show_trace=True):
        self.history = []
        self.show_trace = show_trace

    def reply(self, user_text):
        text = redact(user_text)
        messages = [{"role": "system", "content": SYSTEM}] + self.history + [{"role": "user", "content": text}]
        answer, seen = None, set()
        for step in range(1, MAX_STEPS + 1):
            with span(f"model, step {step}") as s:
                r = client.chat.completions.create(model=MODEL, messages=messages, tools=SPECS, temperature=0)
                s["tokens"] = r.usage.total_tokens if r.usage else None
            msg = r.choices[0].message
            if not msg.tool_calls:
                answer = msg.content or ""
                break
            messages.append(msg)
            for call in msg.tool_calls:
                key = (call.function.name, call.function.arguments)
                args = json.loads(call.function.arguments or "{}")
                if key in seen:
                    result = {"error": "you already called this with the same arguments; answer now"}
                else:
                    seen.add(key)
                    with span(f"tool {call.function.name}", args=args):
                        result = run_tool(call.function.name, args)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        if answer is None:
            answer = "Sorry, I couldn't finish that. Please contact customer service."
        if IBAN.search(answer):
            answer = "[blocked by output guard]"
        self.history += [{"role": "user", "content": text}, {"role": "assistant", "content": answer}]
        self.history = self.history[-MAX_TURNS * 2:]
        if self.show_trace:
            save_and_show(text[:40])               # the redacted text: no personal data in the log
        return answer
