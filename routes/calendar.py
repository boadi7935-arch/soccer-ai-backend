from fastapi import APIRouter, HTTPException
from database.firebase_db import db
from database.store import new_id, now
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class CalendarEvent(BaseModel):
    team_id: str
    title: str
    event_type: str
    date: str
    time: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    coach_name: Optional[str] = "Coach"

@router.post("/")
def create_event(event: CalendarEvent):
    event_id = new_id()
    event_data = {
        **event.dict(),
        "id": event_id,
        "created_at": now()
    }
    db.collection('calendar').document(event_id).set(event_data)
    return event_data

@router.get("/team/{team_id}")
def get_team_events(team_id: str):
    docs = db.collection('calendar').where('team_id', '==', team_id).stream()
    events = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return sorted(events, key=lambda x: x.get('date', ''))

@router.delete("/{event_id}")
def delete_event(event_id: str):
    db.collection('calendar').document(event_id).delete()
    return {"message": "Event deleted"}
