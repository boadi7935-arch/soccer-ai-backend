from fastapi import APIRouter, HTTPException
from database.firebase_db import db
from database.store import new_id, now
from pydantic import BaseModel
from typing import Optional, List
from services.email_service import email_coach_new_request, email_parent_request_received, email_parent_review_complete

router = APIRouter()

class CoachProfile(BaseModel):
    name: str
    email: str
    bio: str
    speciality: List[str]
    certifications: List[str]
    experience_years: int
    rate_video_review: float
    rate_video_zoom: float
    location: str
    languages: Optional[List[str]] = ['English']
    avatar_url: Optional[str] = None
    youtube_url: Optional[str] = None

class ReviewRequest(BaseModel):
    player_id: str
    coach_profile_id: str
    video_url: str
    focus_areas: List[str]
    notes: Optional[str] = None
    include_zoom: bool = False
    amount_paid: float
    player_name: str
    player_age: int
    player_position: str

@router.post("/coaches")
def create_coach_profile(profile: CoachProfile):
    profile_id = new_id()
    data = {
        **profile.dict(),
        "id": profile_id,
        "created_at": now(),
        "verified": False,
        "rating": 0,
        "total_reviews": 0
    }
    db.collection('pro_coaches').document(profile_id).set(data)
    return data

@router.get("/coaches")
def get_all_coaches():
    docs = db.collection('pro_coaches').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

@router.put("/coaches/{coach_id}")
def update_coach_profile(coach_id: str, profile: CoachProfile):
    doc = db.collection('pro_coaches').document(coach_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Coach not found")
    existing = doc.to_dict()
    updated = {
        **existing,
        **profile.dict(),
        "id": coach_id,
    }
    db.collection('pro_coaches').document(coach_id).set(updated)
    return updated

@router.get("/coaches/{coach_id}")
def get_coach(coach_id: str):
    doc = db.collection('pro_coaches').document(coach_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Coach not found")
    return {'id': doc.id, **doc.to_dict()}

@router.post("/requests")
def create_review_request(request: ReviewRequest):
    request_id = new_id()
    data = {
        **request.dict(),
        "id": request_id,
        "created_at": now(),
        "status": "pending",
        "coach_response": None,
        "response_video_url": None,
        "zoom_link": None
    }
    db.collection('pro_reviews').document(request_id).set(data)
    
    # Get coach profile and send emails
    try:
        coach_doc = db.collection('pro_coaches').document(request.coach_profile_id).get()
        if coach_doc.exists:
            coach = coach_doc.to_dict()
            # Email coach
            email_coach_new_request(
                coach_email=coach.get('email'),
                coach_name=coach.get('name'),
                player_name=request.player_name,
                player_age=request.player_age,
                player_position=request.player_position,
                focus_areas=request.focus_areas,
                amount=request.amount_paid
            )
    except Exception as e:
        print(f"Email error: {e}")
    
    return data

@router.get("/requests/all")
def get_all_requests():
    docs = db.collection('pro_reviews').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

@router.get("/requests/player/{player_id}")
def get_player_requests(player_id: str):
    docs = db.collection('pro_reviews').where('player_id', '==', player_id).stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

@router.get("/requests/coach/{coach_profile_id}")
def get_coach_requests(coach_profile_id: str):
    docs = db.collection('pro_reviews').where('coach_profile_id', '==', coach_profile_id).stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

@router.put("/requests/{request_id}/respond")
def respond_to_request(request_id: str, coach_response: str, response_video_url: Optional[str] = None, zoom_link: Optional[str] = None):
    doc = db.collection('pro_reviews').document(request_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Request not found")
    doc_data = db.collection('pro_reviews').document(request_id).get().to_dict()
    db.collection('pro_reviews').document(request_id).update({
        'coach_response': coach_response,
        'response_video_url': response_video_url,
        'zoom_link': zoom_link,
        'status': 'completed'
    })
    
    # Send email to parent
    try:
        coach_doc = db.collection('pro_coaches').document(doc_data.get('coach_profile_id')).get()
        coach_name = coach_doc.to_dict().get('name') if coach_doc.exists else 'Coach'
        player_doc = db.collection('players').document(doc_data.get('player_id')).get()
        if player_doc.exists:
            player = player_doc.to_dict()
            parent_email = player.get('parent_email')
            if parent_email:
                email_parent_review_complete(
                    parent_email=parent_email,
                    player_name=doc_data.get('player_name'),
                    coach_name=coach_name,
                    zoom_link=zoom_link
                )
    except Exception as e:
        print(f"Email error: {e}")
    
    return {"message": "Response submitted"}

@router.delete("/coaches/{coach_id}")
def delete_coach_profile(coach_id: str):
    db.collection('pro_coaches').document(coach_id).delete()
    return {"message": "Coach deleted"}

@router.put("/requests/{request_id}/rate")
def rate_review(request_id: str, rating: int, comment: str = ""):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    doc = db.collection('pro_reviews').document(request_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Request not found")
    
    review = doc.to_dict()
    coach_id = review.get('coach_profile_id')
    
    # Update review with rating
    db.collection('pro_reviews').document(request_id).update({
        'rating': rating,
        'rating_comment': comment,
        'rated_at': now()
    })
    
    # Update coach overall rating
    coach_doc = db.collection('pro_coaches').document(coach_id).get()
    if coach_doc.exists:
        coach = coach_doc.to_dict()
        total_reviews = coach.get('total_reviews', 0) + 1
        current_rating = coach.get('rating', 0)
        new_rating = ((current_rating * (total_reviews - 1)) + rating) / total_reviews
        db.collection('pro_coaches').document(coach_id).update({
            'rating': round(new_rating, 1),
            'total_reviews': total_reviews
        })
    
    return {"message": "Rating submitted", "rating": rating}

@router.put("/requests/{request_id}/status")
def update_status(request_id: str, status: str):
    db.collection('pro_reviews').document(request_id).update({'status': status})
    return {"message": "Status updated"}
