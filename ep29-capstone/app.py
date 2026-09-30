"""
Episode 29 - the finished Nova as a web app (same page as episode 23).
Start it:   uvicorn app:app --port 8000
Then open:  http://localhost:8000
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel

from nova import Nova

HERE = Path(__file__).parent
app = FastAPI()
nova = Nova(show_trace=True)   # one conversation; a real app keeps one per user


class Question(BaseModel):
    text: str


@app.get("/")
def page():
    return FileResponse(HERE / "index.html")


@app.post("/ask")
def ask(question: Question):
    return PlainTextResponse(nova.reply(question.text))
