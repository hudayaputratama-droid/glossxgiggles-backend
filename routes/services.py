from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Service, PricingModifier
from schemas import ServiceCreate, ServiceResponse, ServiceUpdate, PricingModifierCreate, PricingModifierResponse

router = APIRouter()

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Create new service"""
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/", response_model=list[ServiceResponse])
def get_all_services(skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)):
    """Get all services"""
    query = db.query(Service).filter(Service.is_active == True)
    
    if category:
        query = query.filter(Service.category == category)
    
    services = query.offset(skip).limit(limit).all()
    return services

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get service by ID"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, service_update: ServiceUpdate, db: Session = Depends(get_db)):
    """Update service"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    update_data = service_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    db.commit()
    db.refresh(service)
    return service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Soft delete service"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    service.is_active = False
    db.commit()

# Pricing Modifiers
@router.post("/modifiers", response_model=PricingModifierResponse, status_code=status.HTTP_201_CREATED)
def create_pricing_modifier(modifier: PricingModifierCreate, db: Session = Depends(get_db)):
    """Create pricing modifier"""
    db_modifier = PricingModifier(**modifier.dict())
    db.add(db_modifier)
    db.commit()
    db.refresh(db_modifier)
    return db_modifier

@router.get("/{service_id}/modifiers", response_model=list[PricingModifierResponse])
def get_service_modifiers(service_id: int, db: Session = Depends(get_db)):
    """Get pricing modifiers for service"""
    modifiers = db.query(PricingModifier).filter(PricingModifier.service_id == service_id).all()
    return modifiers