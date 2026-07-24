# GLOSS x GIGGLES - SQL Database Schema

## Database: PostgreSQL

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_artist BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    profile_image VARCHAR(500),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Services Table
```sql
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    base_price FLOAT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Pricing Modifiers Table
```sql
CREATE TABLE pricing_modifiers (
    id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL REFERENCES services(id),
    nail_length VARCHAR(50),
    design_complexity VARCHAR(50),
    price_adjustment FLOAT NOT NULL,
    description VARCHAR(255)
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    booking_code VARCHAR(20) UNIQUE,
    customer_id INTEGER NOT NULL REFERENCES users(id),
    artist_id INTEGER REFERENCES users(id),
    service_id INTEGER NOT NULL REFERENCES services(id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL,
    nail_length VARCHAR(50),
    nail_shape VARCHAR(50),
    design_complexity VARCHAR(50),
    notes TEXT,
    inspiration_images VARCHAR(1000),
    base_price FLOAT NOT NULL,
    additional_charges FLOAT DEFAULT 0,
    total_price FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Gallery Table
```sql
CREATE TABLE gallery (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500) NOT NULL,
    artist_id INTEGER NOT NULL REFERENCES users(id),
    nail_length VARCHAR(50),
    nail_shape VARCHAR(50),
    design_complexity VARCHAR(50),
    colors_used VARCHAR(255),
    likes_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Availability Slots Table
```sql
CREATE TABLE availability_slots (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER NOT NULL REFERENCES users(id),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes for Performance

```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_artist ON users(is_artist);
CREATE INDEX idx_services_category ON services(category);
CREATE INDEX idx_bookings_customer_id ON bookings(customer_id);
CREATE INDEX idx_bookings_artist_id ON bookings(artist_id);
CREATE INDEX idx_bookings_appointment_date ON bookings(appointment_date);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_gallery_artist_id ON gallery(artist_id);
CREATE INDEX idx_availability_artist_id ON availability_slots(artist_id);
CREATE INDEX idx_availability_date ON availability_slots(date);
```

## Sample Queries

### Get all services
```sql
SELECT * FROM services WHERE is_active = TRUE;
```

### Get artist bookings for a date
```sql
SELECT b.*, s.name as service_name, u.full_name as customer_name
FROM bookings b
JOIN services s ON b.service_id = s.id
JOIN users u ON b.customer_id = u.id
WHERE b.artist_id = ? AND b.appointment_date = ?
ORDER BY b.appointment_time;
```

### Calculate artist revenue
```sql
SELECT artist_id, SUM(total_price) as total_revenue
FROM bookings
WHERE status = 'completed'
GROUP BY artist_id;
```

### Get available time slots for artist
```sql
SELECT * FROM availability_slots
WHERE artist_id = ? AND date >= TODAY() AND is_available = TRUE
ORDER BY date, start_time;
```

### Get gallery items sorted by popularity
```sql
SELECT * FROM gallery
ORDER BY likes_count DESC, views_count DESC
LIMIT 12;
```
