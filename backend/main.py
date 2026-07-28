"""
FastAPI backend that wires the Smart Whiteboard frontend to the Claude API.

Run with: uvicorn backend.main:app --reload --port 8000
Requires ANTHROPIC_API_KEY to be set in the environment (or a .env file).
"""
import os
from typing import Any, Optional

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_methods=["POST"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()
MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5")

SYSTEM_PROMPT = """You are a Socratic tutor for college-level STEM subjects (statics, circuit analysis).

Rules:
- Never state the final numeric answer or a complete solution.
- Ask one guiding question, or point out one thing to reconsider, per turn.
- If a possible misconception is listed below, address the most critical one first \
by asking a question that surfaces it - do not tell the student "you have a misconception".
- Keep replies to 2-4 sentences.
"""


class AIRequest(BaseModel):
    type: str
    response: Optional[str] = None
    context: dict[str, Any] = {}
    misconceptions: list[dict[str, Any]] = []
    localAnalysis: list[dict[str, Any]] = []


@app.post("/api/ai")
def tutor_turn(req: AIRequest):
    subject = req.context.get("subject", "statics")
    topic = req.context.get("topic", "free_body_diagrams")
    detected = req.misconceptions or req.localAnalysis
    misconception_lines = "\n".join(
        f"- {m.get('description') or m.get('message', 'unspecified issue')}" for m in detected
    )

    user_message = f"""Subject: {subject}
Topic: {topic}
Student said: {req.response or "(no text response - a drawing was submitted)"}

Locally-detected possible misconceptions:
{misconception_lines or "(none detected)"}

Respond as the tutor's next turn."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        output_config={"effort": "medium"},
        messages=[{"role": "user", "content": user_message}],
    )

    if message.stop_reason == "refusal":
        return {"question": "Let's try rephrasing that - can you describe your reasoning differently?", "feedback": None}

    text = next((block.text for block in message.content if block.type == "text"), "")
    return {"question": text, "feedback": None}
