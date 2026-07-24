from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import AvailabilitySlot, User, Booking
from schemas import AvailabilitySlotCreate, AvailabilitySlotResponse
from datetime import date, time, datetime, timedelta

router = APIRouter()

@router.post("/", response_model=AvailabilitySlotResponse, status_code=status.HTTP_201_CREATED)
def create_availability_slot(slot: AvailabilitySlotCreate, db: Session = Depends(get_db)):
    """Create availability slot for artist"""
    # Validate artist exists
    artist = db.query(User).filter(User.id == slot.artist_id, User.is_artist == True).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    db_slot = AvailabilitySlot(**slot.dict())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.get("/artist/{artist_id}", response_model=list[AvailabilitySlotResponse])
def get_artist_availability(artist_id: int, date_from: date = None, date_to: date = None, db: Session = Depends(get_db)):
    """Get availability slots for artist"""
    query = db.query(AvailabilitySlot).filter(
        AvailabilitySlot.artist_id == artist_id,
        AvailabilitySlot.is_available == True
    )
    
    if date_from:
        query = query.filter(AvailabilitySlot.date >= date_from)
    
    if date_to:
        query = query.filter(AvailabilitySlot.date <= date_to)
    
    slots = query.all()
    return slots

@router.get("/artist/{artist_id}/date/{slot_date}", response_model=list[AvailabilitySlotResponse])
def get_artist_availability_by_date(artist_id: int, slot_date: date, db: Session = Depends(get_db)):
    """Get availability slots for artist on specific date"""
    slots = db.query(AvailabilitySlot).filter(
        AvailabilitySlot.artist_id == artist_id,
        AvailabilitySlot.date == slot_date,
        AvailabilitySlot.is_available == True
    ).all()
    return slots

@router.post("/check-availability")
def check_availability(artist_id: int, slot_date: date, start_time: time, duration_minutes: int, db: Session = Depends(get_db)):
    """Check if time slot is available"""
    # Get end time
    start_dt = datetime.combine(slot_date, start_time)
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    end_time = end_dt.time()
    
    # Check for conflicting bookings
    conflicting_booking = db.query(Booking).filter(
        Booking.artist_id == artist_id,
        Booking.appointment_date == slot_date,
        Booking.appointment_time < end_time,
        Booking.status != "cancelled"
    ).first()
    
    if conflicting_booking:
        return {"available": False, "message": "Time slot not available"}
    
    return {"available": True, "message": "Time slot is available"}

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability_slot(slot_id: int, db: Session = Depends(get_db)):
    """Delete availability slot"""
    slot = db.query(AvailabilitySlot).filter(AvailabilitySlot.id == slot_id).first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    
    db.delete(slot)
    db.commit()