from database.firebase_db import db
from datetime import datetime, timedelta

def get_streak(player_id: str) -> dict:
    doc = db.collection('streaks').document(player_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"current_streak": 0, "longest_streak": 0, "last_trained": None, "total_days": 0}

def update_streak(player_id: str) -> dict:
    today = datetime.utcnow().date().isoformat()
    streak_data = get_streak(player_id)
    
    last_trained = streak_data.get("last_trained")
    current_streak = streak_data.get("current_streak", 0)
    longest_streak = streak_data.get("longest_streak", 0)
    total_days = streak_data.get("total_days", 0)

    if last_trained == today:
        return streak_data  # Already trained today

    yesterday = (datetime.utcnow().date() - timedelta(days=1)).isoformat()

    if last_trained == yesterday:
        current_streak += 1  # Consecutive day
    else:
        current_streak = 1  # Reset streak

    if current_streak > longest_streak:
        longest_streak = current_streak

    total_days += 1

    updated = {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_trained": today,
        "total_days": total_days,
        "player_id": player_id
    }
    db.collection('streaks').document(player_id).set(updated)
    return updated

def get_weekly_activity(player_id: str) -> list:
    today = datetime.utcnow().date()
    week = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        week.append(day.isoformat())
    
    feedback_docs = db.collection('feedback').where('player_id', '==', player_id).stream()
    trained_dates = set()
    for doc in feedback_docs:
        data = doc.to_dict()
        created = data.get('created_at', '')
        if created:
            if hasattr(created, 'date'):
                trained_dates.add(created.date().isoformat())
            else:
                trained_dates.add(str(created)[:10])

    return [{"date": d, "trained": d in trained_dates} for d in week]
