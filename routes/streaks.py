from fastapi import APIRouter, HTTPException
from database.streak_db import get_streak, update_streak, get_weekly_activity
from database.firebase_db import get_player

router = APIRouter()

@router.get("/{player_id}")
def get_player_streak(player_id: str):
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    streak = get_streak(player_id)
    activity = get_weekly_activity(player_id)
    return {**streak, "weekly_activity": activity}

@router.post("/{player_id}/train")
def record_training(player_id: str):
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    updated = update_streak(player_id)
    activity = get_weekly_activity(player_id)
    return {**updated, "weekly_activity": activity}
