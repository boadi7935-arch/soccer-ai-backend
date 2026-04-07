from fastapi import APIRouter, HTTPException
from models.schemas import FeedbackCreate, FeedbackResponse, WeeklyPlanRequest
from database.store import feedback_db, assignments_db, players_db, drills_db, new_id, now
from services.ai_feedback import generate_feedback
from services.ai_plan import generate_weekly_plan
import os

router = APIRouter()

@router.post("/generate", response_model=FeedbackResponse)
def generate_ai_feedback(payload: FeedbackCreate):
    player = players_db.get(payload.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    drill = drills_db.get(payload.drill_id)
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")
    
    api_key = os.environ.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail=f"OPENAI_API_KEY not set. Env vars: {list(os.environ.keys())}")
    
    try:
        ai_result = generate_feedback(player, drill, payload.coach_notes or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI feedback failed: {str(e)}")
    
    feedback_id = new_id()
    feedback_data = {
        "id": feedback_id,
        "assignment_id": payload.assignment_id,
        "player_id": payload.player_id,
        "drill_id": payload.drill_id,
        "video_url": payload.video_url,
        "score": ai_result["score"],
        "strength": ai_result["strength"],
        "correction": ai_result["correction"],
        "next_drill_suggestion": ai_result["next_drill_suggestion"],
        "summary": ai_result["summary"],
        "coach_approved": False,
        "created_at": now()
    }
    feedback_db[feedback_id] = feedback_data
    if payload.assignment_id in assignments_db:
        assignments_db[payload.assignment_id]["status"] = "completed"
    return feedback_data

@router.get("/player/{player_id}")
def get_player_feedback_history(player_id: str):
    history = [f for f in feedback_db.values() if f["player_id"] == player_id]
    return sorted(history, key=lambda x: x["created_at"], reverse=True)

@router.get("/{feedback_id}")
def get_feedback(feedback_id: str):
    feedback = feedback_db.get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.put("/{feedback_id}/approve")
def approve_feedback(feedback_id: str, coach_comment: str = ""):
    feedback = feedback_db.get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback_db[feedback_id]["coach_approved"] = True
    if coach_comment:
        feedback_db[feedback_id]["coach_comment"] = coach_comment
    return feedback_db[feedback_id]

@router.post("/weekly-plan")
def get_weekly_plan(payload: WeeklyPlanRequest):
    player = players_db.get(payload.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    api_key = os.environ.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail=f"OPENAI_API_KEY not set. Env vars: {list(os.environ.keys())}")

    player_goals = payload.focus_skills or player["goals"]
    player_level = player["skill_level"]
    available = [d for d in drills_db.values() if d["skill_type"] in player_goals or d["level"] == player_level]
    if not available:
        available = list(drills_db.values())

    try:
        plan = generate_weekly_plan(player, available)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")
    return plan
