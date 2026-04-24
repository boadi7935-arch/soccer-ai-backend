from fastapi import APIRouter, HTTPException
from services.email_service import email_milestone_reached
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
    
    # Check for milestones and send email
    try:
        streak = updated.get('current_streak', 0)
        total = updated.get('total_sessions', 0)
        player = get_player(player_id)
        email = player.get('parent_email') or player.get('email')
        name = player.get('name', 'Player')
        
        milestone = None
        if streak == 7:
            milestone = f"7 Day Streak! 🔥"
        elif streak == 30:
            milestone = f"30 Day Streak! 🔥🔥"
        elif total == 10:
            milestone = f"10 Training Sessions Completed! 💪"
        elif total == 50:
            milestone = f"50 Training Sessions Completed! 🏆"
        
        if milestone and email:
            email_milestone_reached(email, name, milestone)
    except Exception as e:
        print(f"Email error: {e}")
    
    return {**updated, "weekly_activity": activity}
