from fastapi import APIRouter, HTTPException
from models.schemas import PlayerCreate, PlayerResponse
from database.store import players_db, new_id, now

router = APIRouter()

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate):
    player_id = new_id()
    player_data = {**player.dict(), "id": player_id, "created_at": now()}
    players_db[player_id] = player_data
    return player_data

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str):
    player = players_db.get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/")
def list_players():
    return list(players_db.values())

@router.put("/{player_id}")
def update_player(player_id: str, updates: dict):
    player = players_db.get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    players_db[player_id].update(updates)
    return players_db[player_id]
