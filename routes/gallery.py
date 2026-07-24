from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Gallery, User
from schemas import GalleryCreate, GalleryResponse

router = APIRouter()

@router.post("/", response_model=GalleryResponse, status_code=status.HTTP_201_CREATED)
def create_gallery_item(item: GalleryCreate, db: Session = Depends(get_db)):
    """Create new gallery item"""
    # Validate artist exists
    artist = db.query(User).filter(User.id == item.artist_id, User.is_artist == True).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    db_item = Gallery(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[GalleryResponse])
def get_all_gallery_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all gallery items"""
    items = db.query(Gallery).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=GalleryResponse)
def get_gallery_item(item_id: int, db: Session = Depends(get_db)):
    """Get gallery item by ID"""
    item = db.query(Gallery).filter(Gallery.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found"
        )
    return item

@router.get("/artist/{artist_id}", response_model=list[GalleryResponse])
def get_artist_gallery(artist_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get gallery items for artist"""
    items = db.query(Gallery).filter(Gallery.artist_id == artist_id).offset(skip).limit(limit).all()
    return items

@router.post("/{item_id}/like")
def like_gallery_item(item_id: int, db: Session = Depends(get_db)):
    """Like gallery item"""
    item = db.query(Gallery).filter(Gallery.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found"
        )
    
    item.likes_count += 1
    db.commit()
    db.refresh(item)
    return {"likes_count": item.likes_count}

@router.post("/{item_id}/view")
def view_gallery_item(item_id: int, db: Session = Depends(get_db)):
    """Increment view count"""
    item = db.query(Gallery).filter(Gallery.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found"
        )
    
    item.views_count += 1
    db.commit()
    db.refresh(item)
    return {"views_count": item.views_count}