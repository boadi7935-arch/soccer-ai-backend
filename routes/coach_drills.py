from fastapi import APIRouter, HTTPException
from database.firebase_db import db
from database.store import new_id, now
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CoachDrillCreate(BaseModel):
    title: str
    instructions: str
    coaching_points: List[str]
    skill_type: str
    duration_minutes: int
    equipment_needed: Optional[List[str]] = []
    demo_video_url: Optional[str] = None
    assigned_to: List[str]
    coach_name: Optional[str] = "Coach"

@router.post("/")
def create_coach_drill(drill: CoachDrillCreate):
    drill_id = new_id()
    drill_data = {
        **drill.dict(),
        "id": drill_id,
        "created_at": now(),
        "type": "coach_drill"
    }
    db.collection('coach_drills').document(drill_id).set(drill_data)
    return drill_data

@router.get("/player/{player_id}")
def get_coach_drills_for_player(player_id: str):
    docs = db.collection('coach_drills').stream()
    drills = []
    for doc in docs:
        data = doc.to_dict()
        if player_id in data.get('assigned_to', []):
            drills.append({'id': doc.id, **data})
    return drills

@router.get("/")
def get_all_coach_drills():
    docs = db.collection('coach_drills').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

@router.delete("/{drill_id}")
def delete_coach_drill(drill_id: str):
    db.collection('coach_drills').document(drill_id).delete()
    return {"message": "Drill deleted"}
