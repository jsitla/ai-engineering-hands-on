# AI Engineering: Hands-On

The code for the YouTube series **AI Engineering: Hands-On** on [@Shelfze](https://www.youtube.com/@Shelfze).

We build **one AI assistant** from zero, one small step per episode:
a first API call → a chatbot with memory → an assistant that reads your documents (RAG) → a production-ready app → an agent with tools.

Every folder is one episode and runs on its own, so you can start anywhere.

## Quick start

1. Install **Python** (3.10 or newer), **VS Code** and **Ollama** (see Episode 1).
2. Download a small free model:
   ```
   ollama pull llama3.2:3b
   ```
3. Get this code and install the two libraries:
   ```
   git clone https://github.com/jsitla/ai-engineering-hands-on.git
   cd ai-engineering-hands-on
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS / Linux
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`.
5. Check that everything works:
   ```
   cd ep01-setup
   python check_setup.py
   ```

## Free and local, or a paid API: you choose

All code talks to the model through one small file, `llm.py`. Change one line in `.env`:

| `PROVIDER=` | what runs | cost |
|---|---|---|
| `ollama` (default) | a small model on your own computer | free |
| `openai` | OpenAI's API (needs `OPENAI_API_KEY`) | pay per token |
| `anthropic` | Claude through Anthropic's OpenAI-compatible endpoint (needs `ANTHROPIC_API_KEY`) | pay per token |

Anthropic describes its OpenAI-compatible endpoint as a way to test and compare models, not for production apps. Later in the series we also show the native SDKs.

Model names and prices change often. The defaults in `llm.py` were checked on the date in each episode's description; you can override them with `MODEL=` in `.env`.

## Episodes

| # | Episode | Folder |
|---|---|---|
| 1 | Set up your AI workbench | [ep01-setup](ep01-setup) |
| 2 | Your first AI call in 10 lines of Python | [ep02-first-call](ep02-first-call) |
| 3 | Messages, roles and the system prompt | [ep03-roles](ep03-roles) |
| 4 | Tokens, context and cost | [ep04-tokens-cost](ep04-tokens-cost) |
| 5 | Temperature, side by side | [ep05-temperature](ep05-temperature) |
| 6 | Prompting basics that actually work | [ep06-prompting](ep06-prompting) |
| 7 | Get reliable JSON out of AI | [ep07-json](ep07-json) |
| 8 | Build a chatbot that remembers | [ep08-chatbot-memory](ep08-chatbot-memory) |

More episodes are added as they are published.

## Safety

- Never put API keys in your code or commit your `.env` file (it is already in `.gitignore`).
- A small local model makes more mistakes than the big paid ones. That is useful for learning: you will see the problems that the later episodes fix.

## License

MIT
