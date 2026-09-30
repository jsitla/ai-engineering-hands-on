"""
Episode 27 - step 2: fine-tune the small model with LoRA on 120 labelled messages.
Only small extra matrices (the adapter) are trained; the model itself stays frozen.
"""
import random
import time

import torch
from peft import LoraConfig, get_peft_model

from common import DEVICE, HERE, SHORT_PROMPT, build_messages, load, load_model

EPOCHS, LR, BATCH = 5, 4e-4, 8
torch.manual_seed(0)
random.seed(0)

tok, model = load_model()
model.train()
config = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM")
model = get_peft_model(model, config)
for p in model.parameters():
    if p.requires_grad:
        p.data = p.data.float()  # train the adapter in full precision
model.print_trainable_parameters()


def encode(row):
    prompt = tok.apply_chat_template(build_messages(row["text"], SHORT_PROMPT), add_generation_prompt=True, tokenize=False)
    prompt_ids = tok(prompt, add_special_tokens=False)["input_ids"]
    answer_ids = tok(row["label"] + tok.eos_token, add_special_tokens=False)["input_ids"]
    # the model only learns from the answer: prompt positions get label -100 (ignored)
    return prompt_ids + answer_ids, [-100] * len(prompt_ids) + answer_ids


rows = [encode(r) for r in load("train")]
optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=LR)
start = time.perf_counter()
for epoch in range(1, EPOCHS + 1):
    random.shuffle(rows)
    total = 0.0
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i + BATCH]
        width = max(len(ids) for ids, _ in batch)
        input_ids = torch.tensor([ids + [tok.pad_token_id] * (width - len(ids)) for ids, _ in batch], device=DEVICE)
        labels = torch.tensor([lab + [-100] * (width - len(lab)) for _, lab in batch], device=DEVICE)
        mask = torch.tensor([[1] * len(ids) + [0] * (width - len(ids)) for ids, _ in batch], device=DEVICE)
        with torch.autocast(DEVICE, dtype=torch.bfloat16, enabled=DEVICE == "cuda"):
            loss = model(input_ids=input_ids, attention_mask=mask, labels=labels).loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total += loss.item() * len(batch)
    print(f"epoch {epoch}: loss {total / len(rows):.3f}")

model.save_pretrained(HERE / "adapter")
print(f"trained on {len(rows)} examples in {time.perf_counter() - start:.0f} s ({DEVICE})")
print("adapter saved to ep27-fine-tuning/adapter")
