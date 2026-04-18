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

@router.put("/{player_id}")
def update_player(player_id: str, updates: dict):
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    updated = {**player, **updates}
    save_player(player_id, updated)
    return updated
