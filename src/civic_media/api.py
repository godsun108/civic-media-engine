import os
import secrets
import sqlite3
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel
from .models import EditorialBrief
from .storage import connect

app = FastAPI(title="Civic Media Engine", version="0.2.0")

def operator(x_operator_token: str | None = Header(default=None)):
    expected = os.environ.get("CIVIC_MEDIA_TOKEN")
    if not expected or not x_operator_token or not secrets.compare_digest(x_operator_token, expected):
        raise HTTPException(401, "Operator token required")

@app.get("/health")
def health():
    return {"status": "ok", "engine": "civic-media-engine"}

@app.post("/v1/editorial/validate", response_model=EditorialBrief)
def validate_brief(brief: EditorialBrief):
    return brief

@app.post("/v1/editorial", status_code=201, dependencies=[Depends(operator)])
def create_brief(brief: EditorialBrief):
    with connect() as db:
        try:
            db.execute("INSERT INTO briefs(id,payload,status) VALUES (?,?,?)",
                       (brief.id, brief.model_dump_json(), "draft"))
            db.execute("INSERT INTO audit(brief_id,action,actor) VALUES (?,?,?)",
                       (brief.id, "created", "operator"))
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Brief already exists")
    return {"id": brief.id, "status": "draft"}

@app.get("/v1/editorial/{brief_id}", dependencies=[Depends(operator)])
def get_brief(brief_id: str):
    with connect() as db:
        row = db.execute("SELECT payload,status FROM briefs WHERE id=?", (brief_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Brief not found")
    return {"brief": EditorialBrief.model_validate_json(row[0]), "status": row[1]}

class Decision(BaseModel):
    reviewer: str
    note: str

@app.post("/v1/editorial/{brief_id}/submit", dependencies=[Depends(operator)])
def submit_brief(brief_id: str):
    return transition(brief_id, "draft", "pending_review", "submitted", "operator")

@app.post("/v1/editorial/{brief_id}/approve", dependencies=[Depends(operator)])
def approve_brief(brief_id: str, decision: Decision):
    if not decision.reviewer.strip() or not decision.note.strip():
        raise HTTPException(422, "Reviewer and review note required")
    return transition(brief_id, "pending_review", "approved", "approved: " + decision.note, decision.reviewer)

def transition(brief_id, before, after, action, actor):
    with connect() as db:
        result = db.execute("UPDATE briefs SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=? AND status=?",
                            (after, brief_id, before))
        if result.rowcount != 1:
            raise HTTPException(409, "Brief missing or not in required state")
        db.execute("INSERT INTO audit(brief_id,action,actor) VALUES (?,?,?)", (brief_id, action, actor))
    return {"id": brief_id, "status": after}

@app.get("/v1/editorial/{brief_id}/audit", dependencies=[Depends(operator)])
def audit(brief_id: str):
    with connect() as db:
        rows = db.execute("SELECT action,actor,created_at FROM audit WHERE brief_id=? ORDER BY seq",
                          (brief_id,)).fetchall()
    return [{"action": a, "actor": b, "at": c} for a,b,c in rows]
