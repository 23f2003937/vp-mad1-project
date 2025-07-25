from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(200), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')
    
    @property
    def available_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status='A').count()
    
    @property
    def occupied_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status='O').count()
    
    @property
    def reserved_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status='R').count()
    
    def __repr__(self):
        return f'<ParkingLot {self.prime_location_name}>'

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(1), default='A', nullable=False)  # A=Available, R=Reserved, O=Occupied
    
    # Relationships
    reservations = db.relationship('Reservation', backref='parking_spot', lazy=True)
    
    @property
    def current_reservation(self):
        return Reservation.query.filter_by(
            spot_id=self.id, 
            leaving_timestamp=None
        ).first()
    
    def __repr__(self):
        return f'<ParkingSpot {self.spot_number} - {self.status}>'

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    
    @property
    def duration_hours(self):
        if self.leaving_timestamp:
            duration = self.leaving_timestamp - self.parking_timestamp
            return duration.total_seconds() / 3600
        return None
    
    @property
    def calculated_cost(self):
        if self.duration_hours and self.parking_spot:
            return round(self.duration_hours * self.parking_spot.parking_lot.price_per_hour, 2)
        return 0
    
    def __repr__(self):
        return f'<Reservation {self.id} - User {self.user_id}>'
