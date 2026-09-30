"""
Episode 4 - the context window: what happens when the input is too long?

We hide a secret word at the very START of a long text, then ask for it
at the END. If the text no longer fits in the context window, the start
gets cut off, and the model can't know the word.
"""
from llm import MODEL, PROVIDER, get_client

client = get_client()
SECRET = "The secret word is PINEAPPLE. Remember it."
FILLER = "Note {i}: the weekly team meeting moved to Thursday, and the coffee machine on floor two is fixed.\n"

print(f"[{PROVIDER} / {MODEL}]\n")
print(f"{'filler lines':>12} {'tokens read':>12} {'answer':>12}")
for lines in (50, 100, 150, 180, 250, 300, 600):
    text = SECRET + "\n" + "".join(FILLER.format(i=i) for i in range(lines))
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": text + "\nWhat is the secret word? Reply with one word."}],
        temperature=0,
    )
    answer = r.choices[0].message.content.strip()[:30]
    print(f"{lines:>12} {r.usage.prompt_tokens:>12} {answer:>12}")
