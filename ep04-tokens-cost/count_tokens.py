"""
Episode 4 - how many tokens does a message really use?
We ask the model and read the 'usage' numbers it sends back.
"""
from llm import MODEL, PROVIDER, get_client

client = get_client()

texts = {
    "English": "Hello! Can you help me write a short email to my landlord about a broken heater?",
    "Slovenian": "Pozdravljeni! Mi lahko pomagate napisati kratko e-pošto najemodajalcu o pokvarjenem radiatorju?",
}

print(f"[{PROVIDER} / {MODEL}]\n")
for language, text in texts.items():
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": text}],
        max_tokens=1,  # we only want the input count, so ask for almost no answer
    )
    words = len(text.split())
    print(f"{language:<10} {words:>3} words -> {r.usage.prompt_tokens:>3} input tokens")
