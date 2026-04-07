from fastapi import APIRouter, HTTPException
from models.schemas import DrillCreate
from database.store import drills_db, new_id
from database.firebase_db import get_player
from typing import Optional

router = APIRouter()

@router.get("/")
def list_drills(skill_type: Optional[str] = None, level: Optional[str] = None):
    drills = list(drills_db.values())
    if skill_type:
        drills = [d for d in drills if d["skill_type"] == skill_type]
    if level:
        drills = [d for d in drills if d["level"] == level]
    return drills

@router.get("/for-player/{player_id}")
def get_drills_for_player(player_id: str):
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_level = player["skill_level"]
    player_goals = player["goals"]
    matched = []
    for drill in drills_db.values():
        if drill["skill_type"] in player_goals and drill["level"] == player_level:
            matched.append(drill)
    if len(matched) < 3:
        for drill in drills_db.values():
            if drill["skill_type"] in player_goals and drill["level"] == "beginner":
                if drill not in matched:
                    matched.append(drill)
    return matched[:5]

@router.get("/{drill_id}")
def get_drill(drill_id: str):
    drill = drills_db.get(drill_id)
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")
    return drill

@router.post("/")
def create_drill(drill: DrillCreate):
    drill_id = new_id()
    drill_data = {**drill.dict(), "id": drill_id}
    drills_db[drill_id] = drill_data
    return drill_data
