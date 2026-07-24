from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Booking
from payment_service import create_payment_intent, confirm_payment
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    booking_id: int

class PaymentConfirmation(BaseModel):
    payment_intent_id: str

@router.post("/create-intent")
def create_payment(payment_request: PaymentRequest, db: Session = Depends(get_db)):
    """Create payment intent for booking"""
    booking = db.query(Booking).filter(Booking.id == payment_request.booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.payment_status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already paid"
        )
    
    try:
        payment_intent = create_payment_intent(booking.total_price, booking.id)
        return {
            "success": True,
            "payment_intent": payment_intent
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/confirm")
def confirm_booking_payment(payment_confirmation: PaymentConfirmation, db: Session = Depends(get_db)):
    """Confirm payment and update booking status"""
    try:
        payment_info = confirm_payment(payment_confirmation.payment_intent_id)
        
        # Update booking payment status
        booking = db.query(Booking).filter(
            Booking.id == payment_info.get("booking_id")
        ).first()
        
        if booking:
            booking.payment_status = "completed"
            booking.payment_method = "credit_card"
            db.commit()
        
        return {
            "success": True,
            "message": "Payment confirmed",
            "payment_info": payment_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
