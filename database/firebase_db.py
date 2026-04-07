import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import base64

def init_firebase():
    if firebase_admin._apps:
        return
    
    # Try base64 env var first (for Railway)
    b64_creds = os.environ.get("FIREBASE_CREDENTIALS_BASE64")
    if b64_creds:
        creds_json = json.loads(base64.b64decode(b64_creds).decode('utf-8'))
        cred = credentials.Certificate(creds_json)
    else:
        # Fall back to local file
        cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')
        cred = credentials.Certificate(cred_path)
    
    firebase_admin.initialize_app(cred)

init_firebase()
db = firestore.client()

def save_player(player_id: str, player_data: dict):
    db.collection('players').document(player_id).set(player_data)

def get_player(player_id: str):
    doc = db.collection('players').document(player_id).get()
    if doc.exists:
        return {'id': doc.id, **doc.to_dict()}
    return None

def get_all_players():
    docs = db.collection('players').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

def save_assignment(assignment_id: str, assignment_data: dict):
    db.collection('assignments').document(assignment_id).set(assignment_data)

def get_player_assignments(player_id: str):
    docs = db.collection('assignments').where('player_id', '==', player_id).stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

def get_assignment(assignment_id: str):
    doc = db.collection('assignments').document(assignment_id).get()
    if doc.exists:
        return {'id': doc.id, **doc.to_dict()}
    return None

def update_assignment_status(assignment_id: str, status: str):
    db.collection('assignments').document(assignment_id).update({'status': status})

def save_feedback(feedback_id: str, feedback_data: dict):
    db.collection('feedback').document(feedback_id).set(feedback_data)

def get_feedback(feedback_id: str):
    doc = db.collection('feedback').document(feedback_id).get()
    if doc.exists:
        return {'id': doc.id, **doc.to_dict()}
    return None

def get_player_feedback(player_id: str):
    docs = db.collection('feedback').where('player_id', '==', player_id).stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]
