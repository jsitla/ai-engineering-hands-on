"""
Episode 5 - does temperature change how often the answer is RIGHT?
Ten runs per setting, on a question with one correct answer.
"""
from llm import ask

question = "What is the capital of Australia? Reply with the city name only."

for temperature in (0, 1, 1.5, 2):
    answers = [ask(question, temperature=temperature).strip().rstrip(".") for _ in range(10)]
    correct = sum(a.lower() == "canberra" for a in answers)
    wrong = sorted({a[:25] for a in answers if a.lower() != "canberra"})
    print(f"temperature {temperature:<4} correct {correct}/10   other answers: {wrong}")
