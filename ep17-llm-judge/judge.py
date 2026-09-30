"""
Episode 17 - LLM-as-judge: a model grades the answers, and we check how often it agrees
with a human. We also check the simple text checks from episode 16.
"""
import json
from pathlib import Path

from labels import LABELS
from llm import MODEL, get_client

client = get_client()
handbook = Path(__file__).parent.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8")
answers = json.loads(Path(__file__).with_name("answers.json").read_text(encoding="utf-8"))

JUDGE_V1 = f"""You are a strict grader. Below is a shop handbook, a customer question and an answer.
The answer is correct only if its key fact matches the handbook AND it adds nothing false or misleading.
Handbook:
{handbook}"""

JUDGE_V2 = f"""You are a strict grader. Below is a shop handbook, a customer question and an answer.
Grade the answer against the handbook, step by step:
1. If the handbook does NOT cover the question, the answer is correct only if it says it doesn't know.
2. If the handbook covers the question, the answer is correct only if its key fact matches the handbook.
3. The answer is incorrect if it adds any detail that is not in the handbook, or contradicts it.
Examples:
Q: Do you sell bicycles? A: I don't know, that's not in the handbook. -> correct (not covered, says so)
Q: Do you deliver to France? A: Yes, we deliver to France. -> incorrect (the handbook lists the countries, France is not one)
Handbook:
{handbook}"""

SCHEMA = {"type": "object", "properties": {"reason": {"type": "string"}, "correct": {"type": "boolean"}},
          "required": ["reason", "correct"], "additionalProperties": False}


def judge(question, answer, system):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": f"Question: {question}\nAnswer: {answer}\nFirst give a short reason, then the verdict."}],
        response_format={"type": "json_schema", "json_schema": {"name": "verdict", "schema": SCHEMA, "strict": True}},
        temperature=0,
    )
    return json.loads(r.choices[0].message.content)


for version, rows in answers.items():
    human = LABELS[version]
    print(f"{version}")
    print(f"  human: {sum(human)}/15 correct | text checks: {sum(r['pass'] for r in rows)}/15,"
          f" agree with human {sum(r['pass'] == h for r, h in zip(rows, human))}/15")
    for name, system in [("judge v1", JUDGE_V1), ("judge v2", JUDGE_V2)]:
        judged = [judge(r["question"], r["reply"], system) for r in rows]
        agree = sum(j["correct"] == h for j, h in zip(judged, human))
        print(f"  {name}: {sum(j['correct'] for j in judged)}/15 correct, agree with human {agree}/15")
        for r, j, h in zip(rows, judged, human):
            if j["correct"] != h:
                print(f"      disagrees: {r['question'][:38]} -> said {j['correct']}: {j['reason'][:80]}")
