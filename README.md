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

Anthropic describes its OpenAI-compatible endpoint as a way to test and compare models, not for production apps. Some features, like prompt caching, need Anthropic's own SDK (episode 19).

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
| 9 | Stream answers word by word | [ep09-streaming](ep09-streaming) |
| 10 | Let AI use your functions (tool calling) | [ep10-tool-calling](ep10-tool-calling) |
| 11 | Embeddings: search by meaning | [ep11-embeddings](ep11-embeddings) |
| 12 | Chunking: how to cut your documents | [ep12-chunking](ep12-chunking) |
| 13 | Your first RAG: chat with your documents | [ep13-rag](ep13-rag) |
| 14 | Move to a vector database | [ep14-vector-db](ep14-vector-db) |
| 15 | Hybrid search and reranking | [ep15-hybrid-rerank](ep15-hybrid-rerank) |
| 16 | Evals: test your AI like software | [ep16-evals](ep16-evals) |
| 17 | LLM-as-judge | [ep17-llm-judge](ep17-llm-judge) |
| 18 | Errors, retries and timeouts | [ep18-errors-retries](ep18-errors-retries) |
| 19 | Prompt caching | [ep19-prompt-caching](ep19-prompt-caching) |
| 20 | Guardrails: check input and output | [ep20-guardrails](ep20-guardrails) |
| 21 | Tracing: see what your AI app is doing | [ep21-tracing](ep21-tracing) |
| 22 | Make it faster and cheaper | [ep22-faster-cheaper](ep22-faster-cheaper) |
| 23 | Deploy it as a web app | [ep23-web-app](ep23-web-app) |
| 24 | Build an agent loop from scratch | [ep24-agent-loop](ep24-agent-loop) |
| 25 | Build your own MCP server | [ep25-mcp-server](ep25-mcp-server) |
| 26 | An agent with tools and memory | [ep26-agent-memory](ep26-agent-memory) |
| 27 | Fine-tuning: when it's worth it (and how) | [ep27-fine-tuning](ep27-fine-tuning) |
| 28 | Working with images | [ep28-images](ep28-images) |
| 29 | Capstone: the finished assistant | [ep29-capstone](ep29-capstone) |

### Extra libraries
- From episode 14: `pip install -r requirements-part2.txt` (Chroma, BM25, sentence-transformers, FastAPI, uvicorn, MCP, Pillow).
- Episode 27 (fine-tuning): install PyTorch from [pytorch.org](https://pytorch.org/get-started/locally/), then `pip install -r ep27-fine-tuning/requirements.txt`.
- Episode 28 (images): `ollama pull gemma3:4b`. From episode 11: `ollama pull nomic-embed-text`.

### About `llm.py`
Episodes 1–20 use the version shown in those videos. From episode 21 on, `llm.py` reuses one client and talks to `127.0.0.1` instead of `localhost` (episode 21 shows why: on Windows, every new connection to `localhost` could wait about 2 seconds).

## Running every demo at once (Windows)

`tools\run_all.ps1` runs every script and saves the output to `runs\` (that's how the outputs in the videos were recorded).

## Safety

- Never put API keys in your code or commit your `.env` file (it is already in `.gitignore`).
- A small local model makes more mistakes than the big paid ones. That is useful for learning: you will see the problems that the later episodes fix.

## License

MIT
