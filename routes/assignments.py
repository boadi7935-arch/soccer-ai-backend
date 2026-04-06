from fastapi import APIRouter, HTTPException
from models.schemas import AssignmentCreate, AssignmentResponse
from database.store import assignments_db, players_db, drills_db, new_id, now

router = APIRouter()

@router.post("/", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate):
    if assignment.player_id not in players_db:
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
    assignments_db[assignment_id] = assignment_data
    return assignment_data

@router.get("/player/{player_id}")
def get_player_assignments(player_id: str):
    return [a for a in assignments_db.values() if a["player_id"] == player_id]

@router.get("/{assignment_id}")
def get_assignment(assignment_id: str):
    assignment = assignments_db.get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/{assignment_id}/status")
def update_status(assignment_id: str, status: str):
    valid = ["pending", "uploaded", "processing", "completed"]
    if status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    assignment = assignments_db.get(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    assignments_db[assignment_id]["status"] = status
    return assignments_db[assignment_id]

@router.get("/")
def list_assignments():
    return list(assignments_db.values())
