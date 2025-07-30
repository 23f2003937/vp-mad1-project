#!/usr/bin/env python3
"""
Create sample data for the Parking Management System
This ensures we have a properly seeded database with test data
"""

from app import app, db
from models import User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        print("🏗️  Creating sample data for Parking Management System...")
        
        # Create sample users (admin is already created automatically)
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password123'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'password': 'password123'},
            {'username': 'sarah_johnson', 'email': 'sarah@example.com', 'password': 'password123'},
        ]
        
        created_users = []
        for user_data in users_data:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=generate_password_hash(user_data['password']),
                    is_admin=False
                )
                db.session.add(user)
                created_users.append(user)
        
        # Create sample parking lots
        lots_data = [
            {
                'prime_location_name': 'Downtown Mall',
                'price': 2.50,
                'address': '123 Main Street, Downtown District, Metropolitan City',
                'pin_code': '12345',
                'maximum_number_of_spots': 25
            },
            {
                'prime_location_name': 'Business Center',
                'price': 3.00,
                'address': '456 Business Avenue, Corporate District, Metropolitan City',
                'pin_code': '12346',
                'maximum_number_of_spots': 20
            },
            {
                'prime_location_name': 'Airport Terminal',
                'price': 4.50,
                'address': '789 Airport Boulevard, Terminal Area, Metropolitan City',
                'pin_code': '12347',
                'maximum_number_of_spots': 20
            }
        ]
        
        created_lots = []
        for lot_data in lots_data:
            existing_lot = ParkingLot.query.filter_by(prime_location_name=lot_data['prime_location_name']).first()
            if not existing_lot:
                lot = ParkingLot(**lot_data)
                db.session.add(lot)
                created_lots.append(lot)
        
        db.session.commit()
        
        # Create parking spots for each lot
        for lot in created_lots:
            for i in range(1, lot.maximum_number_of_spots + 1):
                spot = ParkingSpot(
                    lot_id=lot.id,
                    spot_number=f"S{i:03d}",
                    status='A'  # All spots start as available
                )
                db.session.add(spot)
        
        db.session.commit()
        
        # Create some sample reservations (completed ones for history)
        if created_users and created_lots:
            for _ in range(5):
                user = random.choice(created_users)
                lot = random.choice(created_lots)
                spot = random.choice(lot.parking_spots)
                
                # Create a completed reservation from the past
                start_time = datetime.utcnow() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 8))
                end_time = start_time + timedelta(hours=random.randint(1, 6))
                duration_hours = (end_time - start_time).total_seconds() / 3600
                total_cost = round(duration_hours * lot.price, 2)
                
                reservation = Reservation(
                    spot_id=spot.id,
                    user_id=user.id,
                    parking_timestamp=start_time,
                    leaving_timestamp=end_time,
                    parking_cost_per_unit_time=lot.price,
                    total_cost=total_cost
                )
                db.session.add(reservation)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print("📊 Database now contains:")
        print(f"   - {User.query.count()} users (including admin)")
        print(f"   - {ParkingLot.query.count()} parking lots")
        print(f"   - {ParkingSpot.query.count()} parking spots")
        print(f"   - {Reservation.query.count()} reservations")
        print()
        print("🔑 Login credentials:")
        print("   Admin: admin / admin123")
        print("   Users: john_doe, jane_smith, mike_wilson, sarah_johnson / password123")

if __name__ == '__main__':
    create_sample_data()