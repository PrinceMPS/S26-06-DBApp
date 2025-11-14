from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.bookings_model import get_all_bookings, add_booking_db, update_booking_db, delete_booking_db, get_booking_by_id

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def bookings_page():
    bookings = get_all_bookings()
    # Convert dates to string for display
    for booking in bookings:
        for key, value in booking.items():
            if hasattr(value, "strftime"):
                booking[key] = value.strftime('%Y-%m-%d')
    return render_template('bookings.html', bookings=bookings)

@bookings_bp.route('/bookings/edit/<int:booking_id>')
def edit_booking(booking_id):
    booking = get_booking_by_id(booking_id)
    if booking:
        # Convert dates to string for form
        for key, value in booking.items():
            if hasattr(value, "strftime"):
                booking[key] = value.strftime('%Y-%m-%d')
    
    bookings = get_all_bookings()
    # Convert dates for table display
    for b in bookings:
        for key, value in b.items():
            if hasattr(value, "strftime"):
                b[key] = value.strftime('%Y-%m-%d')
                
    return render_template('bookings.html', bookings=bookings, editing=booking)

@bookings_bp.route('/bookings', methods=['POST'])
def handle_booking():
    action = request.form.get('action', 'save')
    booking_id = request.form.get('booking_id')
    
    if action == 'delete':
        # Handle delete
        try:
            delete_booking_db(booking_id)
            flash('Booking deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting booking: {str(e)}', 'error')
    else:
        # Handle add/update
        guest_id = request.form.get('guest_id')
        room_id = request.form.get('room_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        # Basic validation
        if not all([guest_id, room_id, start_date, end_date]):
            flash('All fields are required', 'error')
            return redirect(url_for('bookings.bookings_page'))
        
        if start_date >= end_date:
            flash('End date must be after start date', 'error')
            return redirect(url_for('bookings.bookings_page'))
        
        try:
            if booking_id:  # Update existing booking
                update_booking_db(booking_id, guest_id, room_id, start_date, end_date)
                flash('Booking updated successfully!', 'success')
            else:  # Add new booking
                add_booking_db(guest_id, room_id, start_date, end_date)
                flash('Booking added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('bookings.bookings_page'))