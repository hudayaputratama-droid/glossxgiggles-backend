from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Booking, Service, User, BookingStatus, PricingModifier
from schemas import BookingCreate, BookingResponse, BookingUpdate
from datetime import datetime
import random
import string

router = APIRouter()

def generate_booking_code():
    """Generate unique booking code"""
    return "GXG-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create new booking"""
    # Validate customer exists
    customer = db.query(User).filter(User.id == booking.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Validate service exists
    service = db.query(Service).filter(Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Calculate price
    base_price = service.base_price
    additional_charges = 0.0
    
    # Get modifiers
    modifiers = db.query(PricingModifier).filter(
        PricingModifier.service_id == booking.service_id
    ).all()
    
    for modifier in modifiers:
        if modifier.nail_length and modifier.nail_length == booking.nail_length:
            additional_charges += modifier.price_adjustment
        if modifier.design_complexity and modifier.design_complexity == booking.design_complexity:
            additional_charges += modifier.price_adjustment
    
    total_price = base_price + additional_charges
    
    # Create booking
    db_booking = Booking(
        booking_code=generate_booking_code(),
        customer_id=booking.customer_id,
        artist_id=booking.artist_id,
        service_id=booking.service_id,
        appointment_date=booking.appointment_date,
        appointment_time=booking.appointment_time,
        duration_minutes=service.duration_minutes,
        nail_length=booking.nail_length,
        nail_shape=booking.nail_shape,
        design_complexity=booking.design_complexity,
        notes=booking.notes,
        base_price=base_price,
        additional_charges=additional_charges,
        total_price=total_price,
        status=BookingStatus.PENDING
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=list[BookingResponse])
def get_all_bookings(skip: int = 0, limit: int = 100, status: str = None, db: Session = Depends(get_db)):
    """Get all bookings"""
    query = db.query(Booking)
    
    if status:
        query = query.filter(Booking.status == status)
    
    bookings = query.offset(skip).limit(limit).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get booking by ID"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking

@router.get("/customer/{customer_id}", response_model=list[BookingResponse])
def get_customer_bookings(customer_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a customer"""
    bookings = db.query(Booking).filter(Booking.customer_id == customer_id).all()
    return bookings

@router.get("/artist/{artist_id}", response_model=list[BookingResponse])
def get_artist_bookings(artist_id: int, db: Session = Depends(get_db)):
    """Get all bookings for an artist"""
    bookings = db.query(Booking).filter(Booking.artist_id == artist_id).all()
    return bookings

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking_update: BookingUpdate, db: Session = Depends(get_db)):
    """Update booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    update_data = booking_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    return booking

@router.post("/{booking_id}/confirm", response_model=BookingResponse)
def confirm_booking(booking_id: int, db: Session = Depends(get_db)):
    """Confirm booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    booking.status = BookingStatus.CONFIRMED
    db.commit()
    db.refresh(booking)
    return booking

@router.post("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    booking.status = BookingStatus.CANCELLED
    db.commit()
    db.refresh(booking)
    return booking