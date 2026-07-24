from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Booking, Service, User, Gallery
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total_bookings = db.query(Booking).count()
    completed_bookings = db.query(Booking).filter(Booking.status == "completed").count()
    pending_bookings = db.query(Booking).filter(Booking.status == "pending").count()
    
    # Calculate revenue
    total_revenue = db.query(func.sum(Booking.total_price)).filter(
        Booking.status == "completed"
    ).scalar() or 0.0
    
    # This week's bookings
    week_ago = datetime.utcnow() - timedelta(days=7)
    this_week_bookings = db.query(Booking).filter(
        Booking.created_at >= week_ago
    ).count()
    
    return {
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "pending_bookings": pending_bookings,
        "total_revenue": float(total_revenue),
        "this_week_bookings": this_week_bookings,
        "services_count": db.query(Service).count(),
        "artists_count": db.query(User).filter(User.is_artist == True).count(),
        "gallery_items": db.query(Gallery).count()
    }

@router.get("/bookings/recent")
def get_recent_bookings(db: Session = Depends(get_db), limit: int = 10):
    """Get recent bookings"""
    bookings = db.query(Booking).order_by(Booking.created_at.desc()).limit(limit).all()
    return bookings

@router.get("/revenue/daily/{days}")
def get_revenue_by_day(days: int = 30, db: Session = Depends(get_db)):
    """Get daily revenue for the last N days"""
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be between 1 and 365"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    result = db.query(
        func.date(Booking.created_at).label("date"),
        func.sum(Booking.total_price).label("revenue")
    ).filter(
        Booking.created_at >= start_date,
        Booking.status == "completed"
    ).group_by(func.date(Booking.created_at)).all()
    
    return [
        {
            "date": str(row[0]),
            "revenue": float(row[1]) if row[1] else 0.0
        }
        for row in result
    ]

@router.get("/artists/performance")
def get_artists_performance(db: Session = Depends(get_db)):
    """Get artist performance metrics"""
    artists = db.query(User).filter(User.is_artist == True).all()
    
    performance = []
    for artist in artists:
        bookings_count = db.query(Booking).filter(Booking.artist_id == artist.id).count()
        completed_bookings = db.query(Booking).filter(
            Booking.artist_id == artist.id,
            Booking.status == "completed"
        ).count()
        total_revenue = db.query(func.sum(Booking.total_price)).filter(
            Booking.artist_id == artist.id,
            Booking.status == "completed"
        ).scalar() or 0.0
        
        performance.append({
            "artist_id": artist.id,
            "artist_name": artist.full_name,
            "total_bookings": bookings_count,
            "completed_bookings": completed_bookings,
            "total_revenue": float(total_revenue),
            "contact": artist.phone
        })
    
    return performance

@router.get("/services/popular")
def get_popular_services(db: Session = Depends(get_db), limit: int = 5):
    """Get most popular services"""
    popular = db.query(
        Service,
        func.count(Booking.id).label("booking_count")
    ).join(Booking, Service.id == Booking.service_id).group_by(
        Service.id
    ).order_by(func.count(Booking.id).desc()).limit(limit).all()
    
    return [
        {
            "service_id": service.id,
            "service_name": service.name,
            "bookings": count
        }
        for service, count in popular
    ]
