"""
Episode 6 - one more prompting trick: let the model think before it answers.
Five small word problems, answered directly vs step by step.
"""
import re

from llm import ask

PROBLEMS = [
    ("A shop sells mugs for 4 euros each. Ana buys 3 mugs and pays with a 20 euro note. How much change does she get?", 8),
    ("A train leaves at 9:40 and the trip takes 85 minutes. At what minute past 11 does it arrive?", 5),
    ("Marko has 5 boxes with 12 pencils each. He gives away 17 pencils. How many pencils are left?", 43),
    ("A recipe needs 250 g of flour for 10 pancakes. How many grams of flour do you need for 16 pancakes?", 400),
    ("Eva reads 18 pages a day. Her book has 200 pages. After 7 days, how many pages are left?", 74),
]


def last_number(text: str):
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    return float(numbers[-1]) if numbers else None


for name, instruction in [
    ("Answer directly", "Reply with the final number only."),
    ("Think step by step", "Think step by step, then give the final number on the last line."),
]:
    correct = 0
    for question, expected in PROBLEMS:
        answer = ask(f"{question}\n{instruction}", temperature=0)
        correct += last_number(answer) == expected
    print(f"{name:<20} {correct}/{len(PROBLEMS)} correct")
