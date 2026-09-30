"""
llm.py - the one place that decides which AI model we talk to.

Change PROVIDER in the .env file (in the main project folder):
    PROVIDER=ollama      free, runs on your own computer (default)
    PROVIDER=openai      paid API, needs OPENAI_API_KEY
    PROVIDER=anthropic   paid API, needs ANTHROPIC_API_KEY

All three work with the same OpenAI Python library, so the rest
of our code never has to change.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads the .env file, searching upwards from this folder

PROVIDERS = {
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": None,  # a local model needs no key
        "default_model": "llama3.2:3b",
    },
    "openai": {
        "base_url": None,  # None = the normal OpenAI address
        "key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4.1-mini",
    },
    "anthropic": {
        # Anthropic's OpenAI-compatible endpoint. Anthropic describes it
        # as meant for testing and comparing, not for production apps.
        "base_url": "https://api.anthropic.com/v1/",
        "key_env": "ANTHROPIC_API_KEY",
        "default_model": "claude-haiku-4-5",
    },
}

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()
if PROVIDER not in PROVIDERS:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use one of: {', '.join(PROVIDERS)}")

_settings = PROVIDERS[PROVIDER]
MODEL = os.getenv("MODEL") or _settings["default_model"]


def get_client() -> OpenAI:
    """Create a client for the provider chosen in .env."""
    if _settings["key_env"] is None:
        api_key = "ollama"  # Ollama ignores the key, but the library wants one
    else:
        api_key = os.getenv(_settings["key_env"])
        if not api_key:
            raise SystemExit(
                f"PROVIDER={PROVIDER} needs {_settings['key_env']}. "
                "Add it to your .env file or set it in your system."
            )
    return OpenAI(base_url=_settings["base_url"], api_key=api_key)


def ask(prompt: str, system: str | None = None, **settings) -> str:
    """Send one message, get the answer back as text."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = get_client().chat.completions.create(
        model=MODEL, messages=messages, **settings
    )
    return response.choices[0].message.content
