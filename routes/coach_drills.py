from fastapi import APIRouter, HTTPException
from database.firebase_db import db
from database.store import new_id, now
from pydantic import BaseModel
from typing import List, Optional
from services.email_service import email_player_drill_assigned

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
    
    # Send email to each assigned player
    try:
        for player_id in drill.assigned_to:
            player_doc = db.collection('players').document(player_id).get()
            if player_doc.exists:
                player = player_doc.to_dict()
                parent_email = player.get('parent_email')
                player_email = player.get('email')
                email_to = parent_email or player_email
                if email_to:
                    email_player_drill_assigned(
                        player_email=email_to,
                        player_name=player.get('name', 'Player'),
                        drill_title=drill.title,
                        coach_name=drill.coach_name
                    )
    except Exception as e:
        print(f"Email error: {e}")
    
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

@router.put("/{drill_id}/assign")
def reassign_drill(drill_id: str, assigned_to: List[str]):
    doc = db.collection('coach_drills').document(drill_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Drill not found")
    db.collection('coach_drills').document(drill_id).update({'assigned_to': assigned_to})
    return {"message": "Drill reassigned", "assigned_to": assigned_to}

@router.delete("/{drill_id}")
def delete_coach_drill(drill_id: str):
    db.collection('coach_drills').document(drill_id).delete()
    return {"message": "Drill deleted"}
