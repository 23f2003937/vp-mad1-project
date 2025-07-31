# Parking Management System

## Overview

A Flask-based web application for managing 4-wheeler parking lots and reservations. The system supports two user types: **Admins**, who manage parking lots and monitor activity, and **Users**, who can book and manage parking spots in real-time.

---

## Technologies Used

### Backend
- **Flask** – Python web framework
- **Flask-SQLAlchemy** – ORM for database handling
- **Flask-Login** – User authentication and session management
- **Flask-WTF + WTForms** – Form handling and validation
- **Werkzeug** – Password hashing and security utilities

### Frontend
- **Jinja2** – Templating engine for rendering views
- **Bootstrap (Dark Theme)** – Responsive UI framework
- **Feather Icons** – Icon set via CDN
- **Chart.js** – Admin dashboard analytics

### Database
- **SQLite** – Local database (`instance/parkmaster.db`)
- **Models**:
  - `User`
  - `ParkingLot`
  - `ParkingSpot`
  - `Reservation`

---

## User Roles

### Admin
- Auto-created with credentials: `admin / admin`
- Create, edit, and delete parking lots
- Manage parking spots
- View user activity and reservations
- Access analytics via dashboard

### User
- Register and log in
- Book and release parking spots
- Track active and past reservations
- View total parking duration and cost

---

## Core Features

### Authentication
- Role-based access (Admin/User)
- Secure password storage using hashing
- Session-based login/logout system

### Parking Lot & Spot Management
- Define parking lot details (name, address, pin code, price)
- Auto-generate parking spots per lot
- Track availability (`A` = Available, `O` = Occupied)
- Real-time spot updates

### Reservation System
- Automatic spot assignment during booking
- Real-time tracking of start and end times
- Cost calculation based on time parked
- Reservation history per user

### Admin Dashboard
- Overview of system metrics (users, lots, spots, usage)
- Charts for active reservations and availability
- Search and filter by spot number, lot, or status

---

## Data Flow

1. User logs in or registers
2. Browses available parking lots
3. Books a parking spot
4. System auto-assigns the first available spot
5. User starts and ends parking session
6. Cost is calculated and added to reservation history
7. Admin monitors usage and manages lots

---

## Deployment

- Install dependencies: `pip install -r requirements.txt`
- Run the application: `python app.py`
- Database initializes automatically on first run
- Admin account is auto-generated
- Application runs locally at `http://localhost:5000`

---

## Sample Data

- 3 pre-defined parking lots with 65 total spots
- 4 test users for demonstration
- Auto-generated admin user: `admin / admin`

---

## Notes

- Designed specifically for managing 4-wheeler parking spots
- Local SQLite database simplifies testing and deployment
- All major project requirements and features are implemented and functional