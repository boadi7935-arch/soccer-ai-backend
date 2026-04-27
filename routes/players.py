from fastapi import APIRouter, HTTPException
from models.schemas import PlayerCreate, PlayerResponse
from database.store import new_id, now
from database.firebase_db import save_player, get_player, get_all_players

router = APIRouter()

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate):
    player_id = new_id()
    player_data = {
        **player.dict(),
        "id": player_id,
        "created_at": now()
    }
    save_player(player_id, player_data)
    return player_data

@router.get("/{player_id}")
def get_player_route(player_id: str):
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/")
def list_players():
    return get_all_players()

@router.delete("/{player_id}")
def delete_player(player_id: str):
    from database.firebase_db import db
    db.collection('players').document(player_id).delete()
    return {"message": "Player deleted"}

@router.post("/announce")
def announce_to_all(subject: str, message: str):
    from services.email_service import email_announcement
    from database.firebase_db import db
    docs = db.collection('players').stream()
    sent = 0
    failed = 0
    for doc in docs:
        player = doc.to_dict()
        email = player.get('parent_email') or player.get('email')
        if email:
            result = email_announcement(email, subject, message, player.get('name', ''))
            if result:
                sent += 1
            else:
                failed += 1
    return {"sent": sent, "failed": failed, "total": sent + failed}

@router.put("/{player_id}")
def update_player(player_id: str, updates: dict):
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    updated = {**player, **updates}
    save_player(player_id, updated)
    return updated
