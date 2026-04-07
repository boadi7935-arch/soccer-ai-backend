from fastapi import APIRouter, HTTPException
from models.schemas import AssignmentCreate, AssignmentResponse
from database.store import drills_db, new_id, now
from database.firebase_db import save_assignment, get_assignment, get_player_assignments, update_assignment_status, get_player

router = APIRouter()

@router.post("/", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate):
    player = get_player(assignment.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if assignment.drill_id not in drills_db:
        raise HTTPException(status_code=404, detail="Drill not found")
    assignment_id = new_id()
    assignment_data = {
        **assignment.dict(),
        "id": assignment_id,
        "status": "pending",
        "assigned_date": now()
    }
    save_assignment(assignment_id, assignment_data)
    return assignment_data

@router.get("/player/{player_id}")
def get_player_assignments_route(player_id: str):
    return get_player_assignments(player_id)

@router.get("/{assignment_id}")
def get_assignment_route(assignment_id: str):
    assignment = get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/{assignment_id}/status")
def update_status(assignment_id: str, status: str):
    valid = ["pending", "uploaded", "processing", "completed"]
    if status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    assignment = get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    update_assignment_status(assignment_id, status)
    return {**assignment, "status": status}

@router.get("/")
def list_assignments():
    return []
