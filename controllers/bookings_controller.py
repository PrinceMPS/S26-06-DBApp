from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.bookings_model import get_all_bookings, create_booking, update_booking_db, delete_booking_db, \
    get_booking_by_id, get_vacant_rooms, search_guests

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def bookings_page():
    # Initialize empty form data for a new booking
    form_data = {}  # used for editing in template

    bookings = get_all_bookings()
    # Convert dates to string for display
    for booking in bookings:
        for key, value in booking.items():
            if hasattr(value, "strftime"):
                booking[key] = value.strftime('%Y-%m-%d')
    
    # Get vacant rooms for the dropdown
    vacant_rooms = get_vacant_rooms(limit=20)
    
    return render_template('bookings.html', bookings=bookings, editing=form_data, vacant_rooms=vacant_rooms)

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
    
    # Get vacant rooms for the dropdown
    vacant_rooms = get_vacant_rooms(limit=20)
                
    return render_template('bookings.html', bookings=bookings, editing=booking, vacant_rooms=vacant_rooms)

@bookings_bp.route('/bookings', methods=['POST'])
def handle_booking():
    action = request.form.get('action', 'save')
    booking_id = request.form.get('booking_id')

    # Gather form data
    guest_id = request.form.get('guest_id')
    room_id = request.form.get('room_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    form_data = {
        'guest_id': guest_id,
        'room_id': room_id,
        'start_date': start_date,
        'end_date': end_date
    }

    # Handle deletion
    if action == 'delete':
        try:
            delete_booking_db(booking_id)
            flash('Booking deleted successfully! Room status updated to Vacant.', 'success')
        except Exception as e:
            flash(f'Error deleting booking: {str(e)}', 'error')
        return redirect(url_for('bookings.bookings_page'))

    # Handle saving (Add/Update)
    if action == 'save':
        # Basic validation
        if not all([guest_id, room_id, start_date, end_date]):
            flash('All fields are required', 'error')
            vacant_rooms = get_vacant_rooms(limit=20)
            return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data, vacant_rooms=vacant_rooms)

        # Save booking
        try:
            if booking_id:
                # For updates, check if room is changing and handle room status updates
                old_booking = get_booking_by_id(booking_id)
                old_room_id = old_booking['room_id'] if old_booking else None
                
                update_booking_db(booking_id, guest_id, room_id, start_date, end_date)
                
                # Provide informative message about room status changes
                if old_room_id and old_room_id != int(room_id):
                    flash(f'Booking updated successfully! Room {old_room_id} set to Vacant, Room {room_id} set to Reserved.', 'success')
                else:
                    flash('Booking updated successfully!', 'success')
            else:
                # For new bookings, room will be set to Reserved
                create_booking(guest_id, room_id, start_date, end_date)
                flash('Booking added successfully! Room status set to Reserved.', 'success')
        except Exception as e:
            flash(f"Error saving booking: {str(e)}", 'error')
            vacant_rooms = get_vacant_rooms(limit=20)
            return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data, vacant_rooms=vacant_rooms)

    return redirect(url_for('bookings.bookings_page'))

@bookings_bp.route('/bookings/search-guests', methods=['GET'])
def search_guests_route():
    query = request.args.get('q', '')
    if query:
        guests = search_guests(query)
        return jsonify(guests)
    return jsonify([])

@bookings_bp.route('/bookings/vacant-rooms', methods=['GET'])
def get_vacant_rooms_route():
    vacant_rooms = get_vacant_rooms(limit=20)
    return jsonify(vacant_rooms)