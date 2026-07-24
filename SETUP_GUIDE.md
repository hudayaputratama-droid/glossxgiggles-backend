# GLOSS x GIGGLES - Complete Setup Guide

## 📋 Table of Contents
1. [Database Setup](#1-database-setup)
2. [Run Server](#2-run-server)
3. [Frontend Integration](#3-frontend-integration)
4. [Deploy to Production](#4-deploy-to-production)
5. [Additional Features](#5-additional-features)

---

## 1️⃣ Database Setup

### Prerequisites
- Python 3.8+
- PostgreSQL installed and running

### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
- Download from: https://www.postgresql.org/download/windows/
- Run installer and follow instructions

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE glossxgiggles;

# Create user (optional but recommended)
CREATE USER nail_admin WITH PASSWORD 'secure_password_here';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE glossxgiggles TO nail_admin;

# Exit
\\q
```

### Step 3: Configure Connection

Edit `.env` file:

```env
DATABASE_URL=postgresql://nail_admin:secure_password_here@localhost:5432/glossxgiggles
SECRET_KEY=your-super-secret-key-change-this-in-production
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

### Step 4: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\\Scripts\\activate

# Install requirements
pip install -r requirements.txt
```

### Step 5: Verify Database Connection

```bash
python -c "from database import engine; print(engine.connect())"
```

✅ If successful, you'll see a connection object!

---

## 2️⃣ Run Server

### Start Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
Database tables created successfully!
```

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Test API Endpoints

**Register Customer:**
```bash
curl -X POST "http://localhost:8000/api/users/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "customer@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "password": "securepass123"
  }'
```

**Create Service:**
```bash
curl -X POST "http://localhost:8000/api/services" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Gel Manicure",
    "description": "Long-lasting gel polish",
    "category": "manicure",
    "base_price": 40,
    "duration_minutes": 60
  }'
```

**Get All Services:**
```bash
curl http://localhost:8000/api/services
```

---

## 3️⃣ Frontend Integration

### Connect HTML to Backend API

Update your HTML file with JavaScript to communicate with API:

```html
<!-- In your HTML file -->
<script>
const API_URL = 'http://localhost:8000/api';

// Get all services
async function loadServices() {
    try {
        const response = await fetch(`${API_URL}/services`);
        const data = await response.json();
        console.log('Services:', data);
        // Populate services in your HTML
        displayServices(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Display services in HTML
function displayServices(services) {
    const container = document.querySelector('.grid');
    container.innerHTML = services.map(service => `
        <div class="card-hover bg-white rounded-lg shadow-softer p-6">
            <img src="${service.image_url}" alt="${service.name}" class="w-full h-40 object-cover rounded-lg mb-4">
            <h3 class="font-semibold text-lg mb-2">${service.name}</h3>
            <p class="text-gray-600 mb-2">${service.description}</p>
            <div class="flex justify-between items-center">
                <span class="text-primary font-bold">$${service.base_price}</span>
                <span class="text-sm text-gray-500">${service.duration_minutes} mins</span>
            </div>
        </div>
    `).join('');
}

// Create booking
async function createBooking(formData) {
    try {
        const response = await fetch(`${API_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_id: 1,
                service_id: formData.serviceId,
                appointment_date: formData.date,
                appointment_time: formData.time,
                nail_length: formData.nailLength,
                nail_shape: formData.nailShape,
                design_complexity: formData.designComplexity,
                notes: formData.notes
            })
        });
        
        const booking = await response.json();
        console.log('Booking created:', booking);
        // Show confirmation modal
        showBookingConfirmation(booking);
    } catch (error) {
        console.error('Error creating booking:', error);
    }
}

// Load services on page load
document.addEventListener('DOMContentLoaded', loadServices);
</script>
```

### Update Service Selection in Booking Form

```html
<select id="service-select" class="w-full px-4 py-2 border border-gray-300 rounded-lg">
    <option value="">Select a service...</option>
</select>

<script>
async function populateServiceSelect() {
    const response = await fetch('http://localhost:8000/api/services');
    const services = await response.json();
    const select = document.getElementById('service-select');
    
    services.forEach(service => {
        const option = document.createElement('option');
        option.value = service.id;
        option.textContent = `${service.name} - $${service.base_price}`;
        select.appendChild(option);
    });
}

populateServiceSelect();
</script>
```

### Handle Booking Form Submission

```html
<form id="booking-form">
    <!-- Form fields -->
    <button type="submit" class="btn-primary text-white w-full py-3">Complete Booking</button>
</form>

<script>
document.getElementById('booking-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        serviceId: document.querySelector('select[name="service"]').value,
        date: document.querySelector('input[name="date"]').value,
        time: document.querySelector('input[name="time"]').value,
        nailLength: document.querySelector('select[name="nail_length"]').value,
        nailShape: document.querySelector('select[name="nail_shape"]').value,
        designComplexity: document.querySelector('select[name="design_complexity"]').value,
        notes: document.querySelector('textarea[name="notes"]').value
    };
    
    await createBooking(formData);
});
</script>
```

---

## 4️⃣ Deploy to Production

### Option A: Deploy to Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new Heroku app
heroku create glossxgiggles-backend

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main
```

### Option B: Deploy with Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: glossxgiggles
      POSTGRES_USER: nail_admin
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://nail_admin:secure_password@db:5432/glossxgiggles
      SECRET_KEY: your-secret-key
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  postgres_data:
```

Run with Docker:
```bash
docker-compose up
```

### Option C: Deploy to AWS

1. Create EC2 instance (Ubuntu 22.04)
2. SSH into instance
3. Clone repository
4. Setup PostgreSQL RDS
5. Install and run application:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---

## 5️⃣ Additional Features

### Authentication (JWT)

Create `auth.py`:

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return email
```

### Email Notifications

Add to `requirements.txt`:
```
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
```

Create `email_service.py`:

```python
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import settings

conf = ConnectionConfig(
    mail_username=settings.smtp_user,
    mail_password=settings.smtp_password,
    mail_from=settings.smtp_user,
    mail_port=settings.smtp_port,
    mail_server=settings.smtp_server,
    mail_tls=True,
    mail_ssl=False,
)

async def send_booking_confirmation(email: str, booking_code: str):
    message = MessageSchema(
        subject="Booking Confirmation - GLOSS x GIGGLES",
        recipients=[email],
        body=f"Your booking code: {booking_code}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
```

### Payment Integration (Stripe)

Add to `requirements.txt`:
```
stripe==7.0.0
```

Create `payment_service.py`:

```python
import stripe
from config import settings

stripe.api_key = settings.stripe_key

def create_payment_intent(amount: int, booking_id: int):
    intent = stripe.PaymentIntent.create(
        amount=amount * 100,  # Convert to cents
        currency="usd",
        metadata={"booking_id": booking_id}
    )
    return intent
```

### Admin Dashboard

Create `routes/admin.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Booking, Service

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_bookings = db.query(Booking).count()
    completed_bookings = db.query(Booking).filter(Booking.status == "completed").count()
    total_revenue = db.query(Booking).filter(Booking.status == "completed").sum(Booking.total_price)
    
    return {
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "total_revenue": total_revenue,
        "services_count": db.query(Service).count()
    }
```

---

## 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production
- [ ] Setup CORS properly
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Setup logging and monitoring
- [ ] Regular security updates

---

## 📞 Support

For issues or questions:
- Check API docs: http://localhost:8000/docs
- Review error logs
- Test endpoints with curl or Postman
- Contact: hello@glossxgiggles.com

---

**Happy coding! 🚀**
