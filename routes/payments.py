from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

class PaymentIntent(BaseModel):
    amount: float
    currency: str = "usd"
    description: str
    coach_id: str
    player_id: str
    review_type: str

class PaymentConfirm(BaseModel):
    payment_intent_id: str
    review_request_id: str

@router.post("/create-payment-intent")
def create_payment_intent(payment: PaymentIntent):
    try:
        # Convert to cents for Stripe
        amount_cents = int(payment.amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=payment.currency,
            description=payment.description,
            metadata={
                "coach_id": payment.coach_id,
                "player_id": payment.player_id,
                "review_type": payment.review_type
            }
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": payment.amount
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/confirm-payment")
def confirm_payment(data: PaymentConfirm):
    try:
        intent = stripe.PaymentIntent.retrieve(data.payment_intent_id)
        if intent.status == "succeeded":
            return {"success": True, "status": intent.status}
        else:
            return {"success": False, "status": intent.status}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/coach-payout/{coach_id}")
def get_coach_earnings(coach_id: str):
    try:
        # Get all succeeded payments for this coach
        intents = stripe.PaymentIntent.list(limit=100)
        coach_payments = [
            p for p in intents.data
            if p.metadata.get("coach_id") == coach_id
            and p.status == "succeeded"
        ]
        total_earned = sum(p.amount for p in coach_payments) / 100
        platform_cut = total_earned * 0.25
        coach_earnings = total_earned * 0.75
        return {
            "total_reviews": len(coach_payments),
            "total_earned": coach_earnings,
            "platform_cut": platform_cut
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
