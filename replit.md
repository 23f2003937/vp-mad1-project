# Parking Management System

## Overview

This is a Flask-based parking management system that provides separate interfaces for administrators and users. Administrators can manage parking lots and view system analytics, while users can book and manage their parking reservations in real-time.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF with WTForms for form handling and validation
- **Security**: Werkzeug for password hashing and proxy handling

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap (dark theme via CDN)
- **Icons**: Feather Icons
- **Charts**: Chart.js for admin dashboard analytics
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Database Design
- **Primary Database**: PostgreSQL (configurable via DATABASE_URL)
- **Connection Pooling**: Enabled with pool recycling and pre-ping
- **Models**: User, ParkingLot, ParkingSpot, Reservation (implied from code)

## Key Components

### Authentication System
- **User Registration**: Username, email, password with validation
- **Login/Logout**: Session-based authentication
- **Role-based Access**: Admin vs regular user permissions
- **Password Security**: Werkzeug password hashing

### User Management
- **User Model**: Stores username, email, password hash, admin status
- **Profile Management**: Registration and login forms with validation
- **Admin Users**: Special privileges for lot management

### Parking Management
- **Parking Lots**: Location name, pricing, address, pin code, spot capacity
- **Dynamic Spot Allocation**: Automatic spot assignment during booking
- **Real-time Availability**: Live spot counting and status tracking
- **Pricing System**: Hourly rate calculation for reservations

### Reservation System
- **Booking Process**: Select lot, auto-assign spot, start billing
- **Active Reservations**: Track current parking sessions
- **Reservation History**: Complete booking history for users
- **Cost Calculation**: Time-based billing system

### Admin Dashboard
- **System Overview**: Total lots, spots, availability statistics
- **User Management**: View all registered users and their activity
- **Lot Management**: Create, edit, and manage parking facilities
- **Analytics**: Chart-based visualizations for system metrics

## Data Flow

1. **User Registration/Login**: Users create accounts or authenticate
2. **Parking Lot Discovery**: Users browse available lots with real-time spot counts
3. **Reservation Creation**: System auto-assigns first available spot in selected lot
4. **Active Session Management**: Track parking duration and calculate costs
5. **Spot Release**: Users end sessions, spots become available again
6. **Admin Oversight**: Administrators monitor system usage and manage facilities

## External Dependencies

### Frontend Libraries (CDN)
- Bootstrap (Agent Dark Theme)
- Feather Icons
- Chart.js for dashboard analytics

### Python Packages
- Flask and Flask extensions (SQLAlchemy, Login, WTF)
- SQLAlchemy ORM
- Werkzeug security utilities
- WTForms for form validation

### Database
- PostgreSQL as primary database
- SQLAlchemy for database abstraction
- Automatic table creation on startup

## Deployment Strategy

### Environment Configuration
- **Session Security**: Configurable secret key via SESSION_SECRET
- **Database**: PostgreSQL connection via DATABASE_URL environment variable
- **Development Mode**: Debug mode enabled for development
- **Production Ready**: Proxy fix middleware for reverse proxy deployments

### Application Startup
- **Database Initialization**: Automatic table creation
- **Admin User Setup**: Provisions admin user if needed (implied)
- **Host Configuration**: Runs on 0.0.0.0:5000 for container compatibility

### Key Features
- **Real-time Updates**: Dynamic spot availability tracking
- **Responsive Design**: Mobile-friendly interface
- **Role-based Access**: Separate admin and user experiences
- **Form Validation**: Comprehensive client and server-side validation
- **Security**: Password hashing, session management, CSRF protection

## Recent Enhancements (July 25, 2025)

### Enhanced User Dashboard & Parking Workflow
- **Vehicle Status Tracking**: Implemented proper 3-stage workflow: Reserve → Park → Release
- **Real-time Cost Display**: Live cost calculation for active parking sessions
- **One-click Booking**: Direct booking from dashboard parking lot cards
- **Enhanced Status Management**: Support for Reserved (R), Available (A), and Occupied (O) states
- **Improved User Interface**: Better visual feedback and status indicators

### Advanced Admin Features
- **Enhanced Spot Search**: Improved search with comprehensive status display
- **Better Dashboard Analytics**: Enhanced charts and statistics
- **Reserved Spot Tracking**: Full support for tracking reserved vs occupied spots
- **Improved Lot Management**: Better spot allocation when creating/editing lots

### Technical Improvements
- **Enhanced Form Validation**: HTML5 patterns, better error messages, improved UX
- **API Enhancements**: New user chart data endpoints for parking analytics
- **Database Model Fixes**: Resolved all SQLAlchemy constructor issues
- **Error Handling**: Improved feedback and loading states throughout the system