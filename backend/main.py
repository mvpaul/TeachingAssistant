"""
FastAPI backend that wires the Smart Whiteboard frontend to the Claude API.

Run with: uvicorn backend.main:app --reload --port 8000
Requires ANTHROPIC_API_KEY to be set in the environment (or a .env file).
"""
import base64
import os
import uuid
from typing import Any, Optional

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .apns import send_live_activity_update

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


# --- iOS "watch my work" flow ---------------------------------------------
#
# The Broadcast Upload Extension (ios/BroadcastExtension/SampleHandler.swift)
# gates and downsamples frames locally, then posts a subset of them here.
# Session state is in-memory only - fine for a single-backend prototype, but
# won't survive a restart or scale past one process. A real deployment would
# want this in a shared store (Redis, a DB) instead.
SESSIONS: dict[str, dict[str, Any]] = {}


class SessionCreate(BaseModel):
    subject: str
    topic: str


@app.post("/api/session")
def create_session(req: SessionCreate):
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"subject": req.subject, "topic": req.topic, "activity_token": None}
    return {"session_id": session_id}


class ActivityTokenRequest(BaseModel):
    token: str


@app.post("/api/session/{session_id}/activity-token")
def register_activity_token(session_id: str, req: ActivityTokenRequest):
    if session_id in SESSIONS:
        SESSIONS[session_id]["activity_token"] = req.token
    return {"ok": True}


@app.post("/api/analyze-frame")
async def analyze_frame(session_id: str = Form(...), frame: UploadFile = File(...)):
    session = SESSIONS.get(session_id, {})
    subject = session.get("subject", "statics")
    topic = session.get("topic", "free_body_diagrams")

    image_bytes = await frame.read()
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    # effort "low": this fires on every gated frame during a live homework
    # session, so it's tuned for latency/cost over the deepest reasoning -
    # unlike the chat endpoint above, which uses "medium".
    message = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        output_config={"effort": "low"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                {
                    "type": "text",
                    "text": f"Subject: {subject}\nTopic: {topic}\n\n"
                    "This is a screenshot of the student's handwritten work in progress "
                    "(captured from their notes app, not drawn in your own canvas). "
                    "Give the tutor's next turn.",
                },
            ],
        }],
    )

    if message.stop_reason == "refusal":
        return {"question": None, "feedback": None}

    text = next((block.text for block in message.content if block.type == "text"), "")

    token = session.get("activity_token")
    if token and text:
        await send_live_activity_update(token, text)

    return {"question": text, "feedback": None}
