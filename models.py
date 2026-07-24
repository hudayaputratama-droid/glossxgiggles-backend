from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class ServiceCategory(str, enum.Enum):
    MANICURE = "manicure"
    PEDICURE = "pedicure"
    EXTENSIONS = "extensions"
    DESIGN = "design"
    SPA = "spa"

class NailLength(str, enum.Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    EXTRA_LONG = "extra_long"

class NailShape(str, enum.Enum):
    ROUND = "round"
    OVAL = "oval"
    SQUARE = "square"
    ALMOND = "almond"
    STILETTO = "stiletto"

class DesignComplexity(str, enum.Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    ARTISTIC = "artistic"

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), index=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_artist = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    profile_image = Column(String(500))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = relationship("Booking", back_populates="customer")
    artist_bookings = relationship("Booking", back_populates="artist", foreign_keys="Booking.artist_id")
    gallery_items = relationship("Gallery", back_populates="artist")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    category = Column(Enum(ServiceCategory), nullable=False)
    base_price = Column(Float, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = relationship("Booking", back_populates="service")
    pricing_modifiers = relationship("PricingModifier", back_populates="service")

class PricingModifier(Base):
    __tablename__ = "pricing_modifiers"
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    nail_length = Column(Enum(NailLength))
    design_complexity = Column(Enum(DesignComplexity))
    price_adjustment = Column(Float, nullable=False)  # Additional cost
    description = Column(String(255))
    
    # Relationships
    service = relationship("Service", back_populates="pricing_modifiers")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_code = Column(String(20), unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    
    # Appointment Details
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    # Nail Preferences
    nail_length = Column(Enum(NailLength))
    nail_shape = Column(Enum(NailShape))
    design_complexity = Column(Enum(DesignComplexity))
    notes = Column(Text)
    inspiration_images = Column(String(1000))  # JSON array of image URLs
    
    # Pricing
    base_price = Column(Float, nullable=False)
    additional_charges = Column(Float, default=0.0)
    total_price = Column(Float, nullable=False)
    
    # Status
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    payment_status = Column(String(50), default="pending")  # pending, partial, completed
    payment_method = Column(String(50))  # bank_transfer, credit_card, cash
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("User", back_populates="bookings", foreign_keys=[customer_id])
    artist = relationship("User", back_populates="artist_bookings", foreign_keys=[artist_id])
    service = relationship("Service", back_populates="bookings")

class Gallery(Base):
    __tablename__ = "gallery"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(String(500), nullable=False)
    artist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Design Details
    nail_length = Column(Enum(NailLength))
    nail_shape = Column(Enum(NailShape))
    design_complexity = Column(Enum(DesignComplexity))
    colors_used = Column(String(255))  # Comma-separated or JSON
    
    # Engagement
    likes_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    artist = relationship("User", back_populates="gallery_items")

class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)