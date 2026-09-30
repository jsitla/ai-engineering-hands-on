"""
Episode 17 - pairwise judging: instead of "is this answer correct?", ask "which of two answers is better?".
We also swap the order, to check if the judge simply prefers whatever comes first.
"""
import json
from pathlib import Path

from llm import MODEL, get_client

client = get_client()
handbook = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
answers = json.loads(Path(__file__).with_name("answers.json").read_text(encoding="utf-8"))
A, B = answers["A: vector search, 1 chunk"], answers["B: hybrid search, 3 chunks"]
SYSTEM = f"""Compare two answers to a customer question, using the shop handbook below.
The better answer is the one that is correct according to the handbook and adds nothing false.
Reply as JSON: {{"better": "1"}} or {{"better": "2"}}.
Handbook:
{handbook}"""


def pick(question, first, second):
    r = client.chat.completions.create(model=MODEL, temperature=0, response_format={"type": "json_object"}, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Question: {question}\nAnswer 1: {first}\nAnswer 2: {second}"}])
    return json.loads(r.choices[0].message.content).get("better")


wins = {"A": 0, "B": 0}
consistent = 0
compared = 0
for a, b in zip(A, B):
    if a["reply"] == b["reply"]:
        continue                                   # identical answers: nothing to compare
    compared += 1
    first = pick(a["question"], a["reply"], b["reply"])     # A shown first
    second = pick(a["question"], b["reply"], a["reply"])    # B shown first
    winner_1 = "A" if first == "1" else "B"
    winner_2 = "B" if second == "1" else "A"
    if winner_1 == winner_2:
        consistent += 1
        wins[winner_1] += 1
print(f"different answers compared: {compared}")
print(f"judge gave the same winner in both orders: {consistent}/{compared}")
print(f"wins when consistent: A {wins['A']}, B {wins['B']}")
