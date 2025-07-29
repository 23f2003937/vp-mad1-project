from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import app, db
from models import User, ParkingLot, ParkingSpot, Reservation
from forms import LoginForm, RegisterForm, ParkingLotForm, BookParkingForm
from sqlalchemy import func

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password_hash = generate_password_hash(form.password.data)
        user.is_admin = False
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Statistics
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    total_users = User.query.filter_by(is_admin=False).count()
    active_reservations = Reservation.query.filter_by(leaving_timestamp=None).count()
    
    # Recent lots
    recent_lots = ParkingLot.query.order_by(ParkingLot.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_lots=total_lots,
                         total_spots=total_spots,
                         occupied_spots=occupied_spots,
                         available_spots=total_spots - occupied_spots,
                         total_users=total_users,
                         active_reservations=active_reservations,
                         recent_lots=recent_lots)

@app.route('/admin/create_lot', methods=['GET', 'POST'])
@login_required
def create_lot():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('user_dashboard'))
    
    form = ParkingLotForm()
    if form.validate_on_submit():
        lot = ParkingLot()
        lot.prime_location_name = form.prime_location_name.data
        lot.price = form.price.data
        lot.address = form.address.data
        lot.pin_code = form.pin_code.data
        lot.maximum_number_of_spots = form.maximum_number_of_spots.data
        db.session.add(lot)
        db.session.flush()  # Get the ID
        
        # Create parking spots
        if form.maximum_number_of_spots.data:
            for i in range(1, form.maximum_number_of_spots.data + 1):
                spot = ParkingSpot()
                spot.lot_id = lot.id
                spot.spot_number = f"S{i:03d}"
                spot.status = 'A'
                db.session.add(spot)
        
        db.session.commit()
        flash(f'Parking lot "{lot.prime_location_name}" created successfully with {lot.maximum_number_of_spots} spots!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/create_lot.html', form=form)

@app.route('/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
@login_required
def edit_lot(lot_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('user_dashboard'))
    
    lot = ParkingLot.query.get_or_404(lot_id)
    form = ParkingLotForm(obj=lot)
    
    if form.validate_on_submit():
        current_spots = len(lot.parking_spots)
        new_spots = form.maximum_number_of_spots.data or 0
        
        lot.prime_location_name = form.prime_location_name.data
        lot.price = form.price.data
        lot.address = form.address.data
        lot.pin_code = form.pin_code.data
        lot.maximum_number_of_spots = form.maximum_number_of_spots.data
        
        # Adjust parking spots
        if new_spots > current_spots:
            # Add new spots
            for i in range(current_spots + 1, new_spots + 1):
                spot = ParkingSpot()
                spot.lot_id = lot.id
                spot.spot_number = f"S{i:03d}"
                spot.status = 'A'
                db.session.add(spot)
        elif new_spots < current_spots:
            # Remove spots (only if they're available)
            spots_to_remove = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').offset(new_spots).all()
            for spot in spots_to_remove:
                db.session.delete(spot)
        
        db.session.commit()
        flash(f'Parking lot "{lot.prime_location_name}" updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_lot.html', form=form, lot=lot)

@app.route('/admin/delete_lot/<int:lot_id>')
@login_required
def delete_lot(lot_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('user_dashboard'))
    
    lot = ParkingLot.query.get_or_404(lot_id)
    
    # Check if all spots are available
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
    if occupied_spots > 0:
        flash(f'Cannot delete "{lot.prime_location_name}". {occupied_spots} spots are still occupied.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    db.session.delete(lot)
    db.session.commit()
    flash(f'Parking lot "{lot.prime_location_name}" deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_users')
@login_required
def view_users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('user_dashboard'))
    
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/view_users.html', users=users)

@app.route('/admin/search_spot')
@login_required
def search_spot():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    spot_number = request.args.get('spot_number', '').strip()
    if not spot_number:
        return jsonify({'error': 'Spot number required'}), 400
    
    spot = ParkingSpot.query.filter_by(spot_number=spot_number).first()
    if not spot:
        return jsonify({'error': 'Spot not found'}), 404
    
    status_map = {
        'A': 'Available',
        'R': 'Reserved',
        'O': 'Occupied'
    }
    
    result = {
        'spot_number': spot.spot_number,
        'status': status_map.get(spot.status, 'Unknown'),
        'status_code': spot.status,
        'lot_name': spot.parking_lot.prime_location_name,
        'lot_address': spot.parking_lot.address
    }
    
    if spot.status == 'O' and spot.current_reservation:
        reservation = spot.current_reservation
        result['user'] = reservation.user.username
        result['parked_since'] = reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify(result)

@app.route('/admin/search_by_lot')
@login_required
def search_by_lot():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    lot_id = request.args.get('lot_id', '')
    if not lot_id:
        return jsonify({'error': 'Lot ID required'}), 400
    
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'error': 'Parking lot not found'}), 404
    
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    status_map = {'A': 'Available', 'R': 'Reserved', 'O': 'Occupied'}
    
    spot_data = []
    for spot in spots:
        spot_info = {
            'spot_number': spot.spot_number,
            'status': status_map.get(spot.status, 'Unknown'),
            'status_code': spot.status
        }
        
        if spot.status == 'O' and spot.current_reservation:
            reservation = spot.current_reservation
            spot_info['user'] = reservation.user.username
            spot_info['parked_since'] = reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M')
        
        spot_data.append(spot_info)
    
    return jsonify({
        'lot_name': lot.prime_location_name,
        'lot_address': lot.address,
        'total_spots': len(spots),
        'spots': spot_data
    })

@app.route('/admin/search_by_status')
@login_required
def search_by_status():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    status = request.args.get('status', '')
    lot_id = request.args.get('lot_id', '')
    
    query = ParkingSpot.query
    if status:
        query = query.filter_by(status=status)
    if lot_id:
        query = query.filter_by(lot_id=lot_id)
    
    spots = query.all()
    status_map = {'A': 'Available', 'R': 'Reserved', 'O': 'Occupied'}
    
    spot_data = []
    for spot in spots:
        spot_info = {
            'spot_number': spot.spot_number,
            'status': status_map.get(spot.status, 'Unknown'),
            'status_code': spot.status,
            'lot_name': spot.parking_lot.prime_location_name,
            'lot_address': spot.parking_lot.address
        }
        
        if spot.status == 'O' and spot.current_reservation:
            reservation = spot.current_reservation
            spot_info['user'] = reservation.user.username
            spot_info['parked_since'] = reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M')
        
        spot_data.append(spot_info)
    
    return jsonify({
        'total_spots': len(spots),
        'spots': spot_data
    })

# User Routes
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # User's current reservation
    current_reservation = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).first()
    
    # User's completed reservations
    completed_reservations = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.leaving_timestamp.isnot(None)
    ).order_by(Reservation.leaving_timestamp.desc()).limit(5).all()
    
    # Available parking lots
    available_lots = ParkingLot.query.all()
    
    return render_template('user/dashboard.html',
                         current_reservation=current_reservation,
                         completed_reservations=completed_reservations,
                         available_lots=available_lots)

@app.route('/user/book_parking', methods=['GET', 'POST'])
@login_required
def book_parking():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Check if user already has an active reservation
    active_reservation = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).first()
    if active_reservation:
        flash('You already have an active parking reservation. Please release it first.', 'warning')
        return redirect(url_for('user_dashboard'))
    
    form = BookParkingForm()
    if form.validate_on_submit():
        # Find first available spot in selected lot
        available_spot = ParkingSpot.query.filter_by(lot_id=form.lot_id.data, status='A').first()
        
        if not available_spot:
            flash('No available spots in selected parking lot.', 'error')
            return redirect(url_for('book_parking'))
        
        # Create reservation
        reservation = Reservation()
        reservation.spot_id = available_spot.id
        reservation.user_id = current_user.id
        available_spot.status = 'R'  # Reserved status initially
        
        db.session.add(reservation)
        db.session.commit()
        
        flash(f'Parking spot {available_spot.spot_number} reserved successfully at {available_spot.parking_lot.prime_location_name}! Please park your vehicle and mark as occupied.', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('user/book_parking.html', form=form)

@app.route('/user/book_parking_quick/<int:lot_id>', methods=['POST'])
@login_required
def book_parking_quick(lot_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Check if user already has an active reservation
    active_reservation = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).first()
    if active_reservation:
        flash('You already have an active parking reservation. Please release it first.', 'warning')
        return redirect(url_for('user_dashboard'))
    
    # Find first available spot in selected lot
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    
    if not available_spot:
        flash('No available spots in selected parking lot.', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Create reservation
    reservation = Reservation()
    reservation.spot_id = available_spot.id
    reservation.user_id = current_user.id
    reservation.parking_cost_per_unit_time = available_spot.parking_lot.price
    available_spot.status = 'R'  # Reserved status initially
    
    db.session.add(reservation)
    db.session.commit()
    
    lot = available_spot.parking_lot
    flash(f'Parking spot {available_spot.spot_number} reserved successfully at {lot.prime_location_name}! Please park your vehicle and mark as occupied.', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user/mark_parked/<int:reservation_id>')
@login_required
def mark_parked(reservation_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    reservation = Reservation.query.filter_by(id=reservation_id, user_id=current_user.id, leaving_timestamp=None).first_or_404()
    
    # Mark spot as occupied
    reservation.parking_spot.status = 'O'
    db.session.commit()
    
    flash(f'Vehicle marked as parked in spot {reservation.parking_spot.spot_number}. Billing has started.', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user/release_parking/<int:reservation_id>')
@login_required
def release_parking(reservation_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    reservation = Reservation.query.filter_by(id=reservation_id, user_id=current_user.id, leaving_timestamp=None).first_or_404()
    
    # Update reservation
    reservation.leaving_timestamp = datetime.utcnow()
    reservation.total_cost = reservation.calculated_cost
    
    # Update spot status
    reservation.parking_spot.status = 'A'
    
    db.session.commit()
    
    flash(f'Parking spot released successfully. Total cost: ${reservation.total_cost:.2f}', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user/my_bookings')
@login_required
def my_bookings():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.parking_timestamp.desc()).all()
    return render_template('user/my_bookings.html', reservations=reservations)

# API Routes for Charts
@app.route('/api/admin/chart_data')
@login_required
def admin_chart_data():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    # Parking lots data
    lots = ParkingLot.query.all()
    lot_names = [lot.prime_location_name for lot in lots]
    occupied_counts = [lot.occupied_spots_count for lot in lots]
    available_counts = [lot.available_spots_count for lot in lots]
    
    # Revenue data (last 7 days)
    from datetime import timedelta
    today = datetime.utcnow().date()
    revenue_data = []
    dates = []
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        daily_revenue = db.session.query(func.sum(Reservation.total_cost)).filter(
            func.date(Reservation.leaving_timestamp) == date
        ).scalar() or 0
        revenue_data.append(float(daily_revenue))
        dates.append(date.strftime('%m/%d'))
    
    return jsonify({
        'lots': {
            'names': lot_names,
            'occupied': occupied_counts,
            'available': available_counts
        },
        'revenue': {
            'dates': dates,
            'amounts': revenue_data
        }
    })

@app.route('/api/user/chart_data')
@login_required
def user_chart_data():
    if current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    # User's parking history (last 10 reservations)
    reservations = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.leaving_timestamp.isnot(None)
    ).order_by(Reservation.leaving_timestamp.desc()).limit(10).all()
    
    dates = [res.leaving_timestamp.strftime('%m/%d') for res in reversed(reservations)]
    costs = [float(res.total_cost or 0) for res in reversed(reservations)]
    durations = [res.duration_hours or 0 for res in reversed(reservations)]
    
    return jsonify({
        'dates': dates,
        'costs': costs,
        'durations': durations
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html'), 500
