from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from app.graph import build_graph

app = FastAPI(title="AutoStream Agent API")

graph = build_graph()
sessions: Dict[str, dict] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.get("/")
def home():
    return {"status": "running", "service": "AutoStream Agent API"}


@app.post("/chat")
def chat(req: ChatRequest):
    state = sessions.get(req.session_id, {"messages": []})

    result = graph.invoke({
        **state,
        "user_input": req.message
    })

    sessions[req.session_id] = result

    return {
        "session_id": req.session_id,
        "reply": result["reply"]
    }


@app.post("/reset/{session_id}")
def reset_chat(session_id: str):
    sessions.pop(session_id, None)
    return {"message": "session cleared"}