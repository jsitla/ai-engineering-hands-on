"""
Episode 4 - how many tokens does a message really use?
We ask the model and read the 'usage' numbers it sends back.
"""
from llm import MODEL, PROVIDER, get_client

client = get_client()


def input_tokens(text: str) -> int:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": text}],
        max_tokens=1,  # we only want the input count, so ask for almost no answer
    )
    return r.usage.prompt_tokens


print(f"[{PROVIDER} / {MODEL}]\n")
template = input_tokens("Hi")
print(f"Just 'Hi'   -> {template} input tokens (mostly the chat template)\n")

texts = {
    "English": "Hello! Can you help me write a short email to my landlord about a broken heater?",
    "Slovenian": "Pozdravljeni! Mi lahko pomagate napisati kratko e-pošto najemodajalcu o pokvarjenem radiatorju?",
}
for language, text in texts.items():
    total = input_tokens(text)
    words = len(text.split())
    print(f"{language:<10} {words:>3} words -> {total:>3} input tokens, about {total - template + 1} for the message itself")
