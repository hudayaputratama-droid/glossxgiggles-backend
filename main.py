from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import create_tables

# Import routers
from routes import services, bookings, users, gallery, availability

# Initialize FastAPI app
app = FastAPI(
    title="GLOSS x GIGGLES API",
    description="Backend API for Nail Art Studio Booking System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def startup():
    create_tables()
    print("Database tables created successfully!")

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(gallery.router, prefix="/api/gallery", tags=["Gallery"])
app.include_router(availability.router, prefix="/api/availability", tags=["Availability"])

# Health check
@app.get("/")
def read_root():
    return {
        "message": "Welcome to GLOSS x GIGGLES API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port
    )