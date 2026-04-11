from fastapi import APIRouter, HTTPException
from database.firebase_db import db
from database.store import new_id, now
from pydantic import BaseModel
from typing import Optional
import random
import string

router = APIRouter()

def generate_join_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class TeamCreate(BaseModel):
    name: str
    coach_name: str
    age_group: Optional[str] = None
    description: Optional[str] = None

@router.post("/")
def create_team(team: TeamCreate):
    team_id = new_id()
    join_code = generate_join_code()
    team_data = {
        **team.dict(),
        "id": team_id,
        "join_code": join_code,
        "player_ids": [],
        "created_at": now()
    }
    db.collection('teams').document(team_id).set(team_data)
    return team_data

@router.get("/code/{join_code}")
def get_team_by_code(join_code: str):
    docs = db.collection('teams').where('join_code', '==', join_code.upper()).stream()
    teams = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    if not teams:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams[0]

@router.post("/{team_id}/join/{player_id}")
def join_team(team_id: str, player_id: str):
    doc = db.collection('teams').document(team_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    team = doc.to_dict()
    player_ids = team.get('player_ids', [])
    if player_id not in player_ids:
        player_ids.append(player_id)
        db.collection('teams').document(team_id).update({'player_ids': player_ids})
    return {**team, 'id': team_id, 'player_ids': player_ids}

@router.get("/{team_id}")
def get_team(team_id: str):
    doc = db.collection('teams').document(team_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    return {'id': doc.id, **doc.to_dict()}

@router.get("/coach/{coach_name}")
def get_coach_teams(coach_name: str):
    docs = db.collection('teams').where('coach_name', '==', coach_name).stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

@router.get("/{team_id}/players")
def get_team_players(team_id: str):
    doc = db.collection('teams').document(team_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Team not found")
    team = doc.to_dict()
    player_ids = team.get('player_ids', [])
    players = []
    for pid in player_ids:
        pdoc = db.collection('players').document(pid).get()
        if pdoc.exists:
            players.append({'id': pdoc.id, **pdoc.to_dict()})
    return players
