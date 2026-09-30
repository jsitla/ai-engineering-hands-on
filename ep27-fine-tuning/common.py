"""
Episode 27 - shared bits: the data, the prompts, and a helper to ask the small model.
"""
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging as hf_logging

hf_logging.set_verbosity_error()   # keep the output clean: no progress bars or warnings
hf_logging.disable_progress_bar()

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"  # small, open, about 1 GB download
LABELS = ["delivery", "returns", "damaged", "payment", "gift_cards", "account"]
HERE = Path(__file__).parent
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# The short instruction the fine-tuned model is trained with
SHORT_PROMPT = "Label the customer message."

# The long instruction a normal model needs: the rules, plus one example per label
LONG_PROMPT = f"""You sort customer messages for an online home shop.
Reply with exactly one label from this list: {", ".join(LABELS)}.
delivery = shipping, tracking, delivery times and costs.
returns = sending something back, refunds, exchanges.
damaged = broken, faulty or damaged products, warranty.
payment = paying, charges, invoices, VAT.
gift_cards = gift cards and discount codes.
account = login, passwords, account settings, personal data.
Reply with the label only."""

EXAMPLES = [
    ("My order hasn't arrived yet.", "delivery"),
    ("I want to send the chair back.", "returns"),
    ("The vase arrived broken.", "damaged"),
    ("Can I pay by bank transfer?", "payment"),
    ("My discount code doesn't work.", "gift_cards"),
    ("I forgot my password.", "account"),
]


def load(name: str) -> list[dict]:
    with open(HERE / "data" / f"{name}.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_model(adapter: str | None = None):
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    dtype = torch.bfloat16 if DEVICE == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, dtype=dtype).to(DEVICE)
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, HERE / adapter)
    model.eval()
    return tok, model


def build_messages(text: str, system: str, examples=()) -> list[dict]:
    messages = [{"role": "system", "content": system}]
    for q, a in examples:
        messages += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]
    return messages + [{"role": "user", "content": text}]


def score(tok, model, system: str, examples=(), name: str = "") -> None:
    rows = load("test")
    correct, prompt_tokens, wrong = 0, 0, []
    start = time.perf_counter()
    for row in rows:
        messages = build_messages(row["text"], system, examples)
        prompt = tok.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
        ids = tok(prompt, return_tensors="pt", add_special_tokens=False)["input_ids"].to(DEVICE)
        prompt_tokens += ids.shape[1]
        with torch.no_grad():
            out = model.generate(ids, max_new_tokens=6, do_sample=False, pad_token_id=tok.eos_token_id)
        answer = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip().lower().strip(".")
        if answer == row["label"]:
            correct += 1
        else:
            wrong.append(f"{row['text'][:45]!r} -> {answer!r} (should be {row['label']})")
    seconds = time.perf_counter() - start
    print(f"--- {name} ---")
    for w in wrong[:5]:
        print("  X", w)
    print(f"correct: {correct}/{len(rows)}   prompt tokens per message: {prompt_tokens // len(rows)}"
          f"   time: {seconds / len(rows):.2f} s per message")
