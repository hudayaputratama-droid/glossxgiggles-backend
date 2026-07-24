from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date, time
from typing import Optional, List
from enum import Enum

# Enums
class ServiceCategoryEnum(str, Enum):
    MANICURE = "manicure"
    PEDICURE = "pedicure"
    EXTENSIONS = "extensions"
    DESIGN = "design"
    SPA = "spa"

class NailLengthEnum(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    EXTRA_LONG = "extra_long"

class NailShapeEnum(str, Enum):
    ROUND = "round"
    OVAL = "oval"
    SQUARE = "square"
    ALMOND = "almond"
    STILETTO = "stiletto"

class DesignComplexityEnum(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    ARTISTIC = "artistic"

class BookingStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_artist: bool
    is_admin: bool
    is_active: bool
    profile_image: Optional[str]
    bio: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Service Schemas
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: ServiceCategoryEnum
    base_price: float
    duration_minutes: int
    image_url: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    duration_minutes: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Pricing Modifier Schemas
class PricingModifierCreate(BaseModel):
    service_id: int
    nail_length: Optional[NailLengthEnum] = None
    design_complexity: Optional[DesignComplexityEnum] = None
    price_adjustment: float
    description: Optional[str] = None

class PricingModifierResponse(PricingModifierCreate):
    id: int
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingCreate(BaseModel):
    customer_id: int
    service_id: int
    appointment_date: date
    appointment_time: time
    nail_length: Optional[NailLengthEnum] = None
    nail_shape: Optional[NailShapeEnum] = None
    design_complexity: Optional[DesignComplexityEnum] = None
    notes: Optional[str] = None
    artist_id: Optional[int] = None

class BookingUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    nail_length: Optional[NailLengthEnum] = None
    nail_shape: Optional[NailShapeEnum] = None
    design_complexity: Optional[DesignComplexityEnum] = None
    notes: Optional[str] = None
    status: Optional[BookingStatusEnum] = None

class BookingResponse(BaseModel):
    id: int
    booking_code: str
    customer_id: int
    artist_id: Optional[int]
    service_id: int
    appointment_date: date
    appointment_time: time
    nail_length: Optional[NailLengthEnum]
    nail_shape: Optional[NailShapeEnum]
    design_complexity: Optional[DesignComplexityEnum]
    notes: Optional[str]
    base_price: float
    additional_charges: float
    total_price: float
    status: BookingStatusEnum
    payment_status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Gallery Schemas
class GalleryCreate(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    artist_id: int
    nail_length: Optional[NailLengthEnum] = None
    nail_shape: Optional[NailShapeEnum] = None
    design_complexity: Optional[DesignComplexityEnum] = None
    colors_used: Optional[str] = None

class GalleryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image_url: str
    artist_id: int
    nail_length: Optional[NailLengthEnum]
    nail_shape: Optional[NailShapeEnum]
    design_complexity: Optional[DesignComplexityEnum]
    colors_used: Optional[str]
    likes_count: int
    views_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Availability Schemas
class AvailabilitySlotCreate(BaseModel):
    artist_id: int
    date: date
    start_time: time
    end_time: time

class AvailabilitySlotResponse(AvailabilitySlotCreate):
    id: int
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True