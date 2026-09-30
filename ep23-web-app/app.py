"""
Episode 23 - Nova as a web app: a small API + a chat page in the browser.
Start it:   uvicorn app:app --port 8000
Then open:  http://localhost:8000
"""
import math
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from chunkers import by_section
from llm import MODEL, embed, get_client

HERE = Path(__file__).parent
client = get_client()
chunks = by_section(HERE.parent.joinpath("data", "northwind_handbook.md").read_text(encoding="utf-8"))
vectors = embed(chunks)   # once, when the server starts
SYSTEM = """You are Nova, the assistant of the shop Northwind Home.
Use ONLY the context. If the answer is not there, say you don't know. One or two sentences."""

app = FastAPI()


class Question(BaseModel):
    text: str


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


@app.get("/")
def page():
    return FileResponse(HERE / "index.html")


@app.post("/ask")
def ask(question: Question):
    q = embed([question.text])[0]
    top = sorted(range(len(chunks)), key=lambda i: cosine(q, vectors[i]), reverse=True)[:3]
    context = "\n\n".join(chunks[i] for i in top)
    stream = client.chat.completions.create(model=MODEL, temperature=0, stream=True, messages=[
        {"role": "system", "content": SYSTEM}, {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question.text}"}])

    def pieces():
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(pieces(), media_type="text/plain")
