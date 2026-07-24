# GLOSS x GIGGLES - Backend API

**Premium Nail Art Studio Booking System**

## Overview

This is a FastAPI-based backend for the GLOSS x GIGGLES nail art studio booking system. It provides REST API endpoints for managing services, bookings, artists, gallery, and customer information.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Server**: Uvicorn
- **Authentication**: JWT (ready to implement)
- **Password Hashing**: bcrypt

## Features

✅ User Management (Customers & Artists)
✅ Service Management with Pricing Modifiers
✅ Booking System with Automatic Price Calculation
✅ Gallery Management
✅ Availability Slot Management
✅ Conflict Detection for Bookings
✅ CORS Support
✅ Automatic API Documentation (Swagger UI)

## Project Structure

```
glossxgiggles-backend/
├── main.py              # FastAPI app initialization
├── config.py            # Configuration settings
├── database.py          # Database setup and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for API validation
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── routes/
    ├── users.py         # User endpoints
    ├── services.py      # Service endpoints
    ├── bookings.py      # Booking endpoints
    ├── gallery.py       # Gallery endpoints
    └── availability.py  # Availability endpoints
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/hudayaputratama-droid/glossxgiggles-backend.git
cd glossxgiggles-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database

First, ensure PostgreSQL is installed and running:

```bash
# Create PostgreSQL database
createb glossxgiggles
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your database credentials:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/glossxgiggles
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

### 6. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Users
- `POST /api/users/register` - Register new user
- `GET /api/users/me/{user_id}` - Get user profile
- `PUT /api/users/me/{user_id}` - Update user profile
- `GET /api/users/artists` - Get all artists
- `GET /api/users/artists/{artist_id}` - Get specific artist

### Services
- `POST /api/services` - Create service
- `GET /api/services` - Get all services
- `GET /api/services/{service_id}` - Get specific service
- `PUT /api/services/{service_id}` - Update service
- `DELETE /api/services/{service_id}` - Delete service
- `POST /api/services/modifiers` - Create pricing modifier
- `GET /api/services/{service_id}/modifiers` - Get service modifiers

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings` - Get all bookings
- `GET /api/bookings/{booking_id}` - Get specific booking
- `GET /api/bookings/customer/{customer_id}` - Get customer bookings
- `GET /api/bookings/artist/{artist_id}` - Get artist bookings
- `PUT /api/bookings/{booking_id}` - Update booking
- `POST /api/bookings/{booking_id}/confirm` - Confirm booking
- `POST /api/bookings/{booking_id}/cancel` - Cancel booking

### Gallery
- `POST /api/gallery` - Create gallery item
- `GET /api/gallery` - Get all gallery items
- `GET /api/gallery/{item_id}` - Get specific item
- `GET /api/gallery/artist/{artist_id}` - Get artist's gallery
- `POST /api/gallery/{item_id}/like` - Like item
- `POST /api/gallery/{item_id}/view` - View item

### Availability
- `POST /api/availability` - Create availability slot
- `GET /api/availability/artist/{artist_id}` - Get artist availability
- `GET /api/availability/artist/{artist_id}/date/{slot_date}` - Get availability by date
- `POST /api/availability/check-availability` - Check if slot is available
- `DELETE /api/availability/{slot_id}` - Delete availability slot

## Database Schema

### Tables
1. **users** - Customer and artist profiles
2. **services** - Available services
3. **pricing_modifiers** - Price adjustments based on nail preferences
4. **bookings** - Customer appointments
5. **gallery** - Nail design portfolio
6. **availability_slots** - Artist working hours

## Authentication (Ready to Implement)

The project includes bcrypt for password hashing. JWT authentication can be added by:

1. Creating a `auth.py` file for token generation/validation
2. Adding JWT dependencies to protected routes
3. Implementing login endpoint

## Example Usage

### Register Customer
```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "password": "secure_password"
  }'
```

### Create Service
```bash
curl -X POST "http://localhost:8000/api/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gel Manicure",
    "description": "Long-lasting gel polish",
    "category": "manicure",
    "base_price": 40,
    "duration_minutes": 60
  }'
```

### Create Booking
```bash
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "service_id": 1,
    "appointment_date": "2024-12-25",
    "appointment_time": "14:00",
    "nail_length": "medium",
    "nail_shape": "almond",
    "design_complexity": "complex"
  }'
```

## Development

### Running with Hot Reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations (Future)
For production, consider using Alembic for database migrations.

## Deployment

### Using Gunicorn (Production)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Using Docker (Recommended)
Dockerfile coming soon!

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License

## Support

For questions or issues, please contact: hello@glossxgiggles.com
