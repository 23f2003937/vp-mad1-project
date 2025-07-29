#!/usr/bin/env python3
"""
Script to create sample data for the Vehicle Parking App - V1
This demonstrates all the functionality with SQLite database
"""

from app import app, db
from models import User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        print("Creating sample data for Vehicle Parking App - V1...")
        
        # Create sample parking lots
        lots_data = [
            {
                'prime_location_name': 'Downtown Shopping Mall',
                'price': 3.50,
                'address': '123 Main Street, Downtown Area, City Center',
                'pin_code': '12345',
                'maximum_number_of_spots': 20
            },
            {
                'prime_location_name': 'Business District Plaza',
                'price': 5.00,
                'address': '456 Business Avenue, Financial District',
                'pin_code': '54321',
                'maximum_number_of_spots': 15
            },
            {
                'prime_location_name': 'Airport Terminal Parking',
                'price': 8.00,
                'address': '789 Airport Road, Terminal 1, International Airport',
                'pin_code': '67890',
                'maximum_number_of_spots': 30
            }
        ]
        
        # Create parking lots
        created_lots = []
        for lot_data in lots_data:
            existing_lot = ParkingLot.query.filter_by(prime_location_name=lot_data['prime_location_name']).first()
            if not existing_lot:
                lot = ParkingLot(**lot_data)
                db.session.add(lot)
                db.session.flush()  # Get the ID
                
                # Create parking spots for this lot
                for i in range(1, lot_data['maximum_number_of_spots'] + 1):
                    spot = ParkingSpot()
                    spot.lot_id = lot.id
                    spot.spot_number = f"S{i:03d}"
                    spot.status = 'A'  # All spots start as Available
                    db.session.add(spot)
                
                created_lots.append(lot)
                print(f"✓ Created lot: {lot.prime_location_name} with {lot_data['maximum_number_of_spots']} spots")
        
        # Create sample users
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password123'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'password': 'password123'},
            {'username': 'sarah_johnson', 'email': 'sarah@example.com', 'password': 'password123'}
        ]
        
        created_users = []
        for user_data in users_data:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User()
                user.username = user_data['username']
                user.email = user_data['email']
                user.password_hash = generate_password_hash(user_data['password'])
                user.is_admin = False
                db.session.add(user)
                created_users.append(user)
                print(f"✓ Created user: {user.username}")
        
        db.session.commit()
        
        # Create some sample reservations to show occupied and reserved spots
        if created_lots and created_users:
            # Make some spots occupied
            spots_to_occupy = []
            for lot in created_lots[:2]:  # Use first 2 lots
                available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').limit(3).all()
                spots_to_occupy.extend(available_spots)
            
            for i, spot in enumerate(spots_to_occupy[:4]):  # Occupy 4 spots
                if i < len(created_users):
                    reservation = Reservation()
                    reservation.spot_id = spot.id
                    reservation.user_id = created_users[i].id
                    reservation.parking_timestamp = datetime.utcnow() - timedelta(hours=random.randint(1, 5))
                    reservation.parking_cost_per_unit_time = spot.parking_lot.price
                    
                    spot.status = 'O'  # Occupied
                    db.session.add(reservation)
                    print(f"✓ Created active reservation: {spot.spot_number} by {created_users[i].username}")
            
            # Make some spots reserved
            reserved_spots = ParkingSpot.query.filter_by(status='A').limit(2).all()
            for i, spot in enumerate(reserved_spots):
                if i < len(created_users):
                    reservation = Reservation()
                    reservation.spot_id = spot.id
                    reservation.user_id = created_users[i].id
                    reservation.parking_cost_per_unit_time = spot.parking_lot.price
                    # No parking_timestamp yet (just reserved, not parked)
                    
                    spot.status = 'R'  # Reserved
                    db.session.add(reservation)
                    print(f"✓ Created reservation: {spot.spot_number} reserved by {created_users[i].username}")
        
        db.session.commit()
        print("\n✅ Sample data created successfully!")
        print("\nDemo Credentials:")
        print("Admin: username=admin, password=admin123")
        print("Users: john_doe, jane_smith, mike_wilson, sarah_johnson (all with password=password123)")
        
        # Print summary
        total_lots = ParkingLot.query.count()
        total_spots = ParkingSpot.query.count()
        total_users = User.query.filter_by(is_admin=False).count()
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()
        reserved_spots = ParkingSpot.query.filter_by(status='R').count()
        available_spots = ParkingSpot.query.filter_by(status='A').count()
        
        print(f"\n📊 Database Summary:")
        print(f"Total Parking Lots: {total_lots}")
        print(f"Total Parking Spots: {total_spots}")
        print(f"  - Available: {available_spots}")
        print(f"  - Reserved: {reserved_spots}")
        print(f"  - Occupied: {occupied_spots}")
        print(f"Total Users: {total_users}")
        print(f"Active Reservations: {Reservation.query.filter_by(leaving_timestamp=None).count()}")

if __name__ == '__main__':
    create_sample_data()