from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.bookings_model import get_all_bookings, create_booking, get_vacant_rooms, search_guests

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def bookings_page():
    bookings = get_all_bookings()
    vacant_rooms = get_vacant_rooms(limit=20)
    return render_template('bookings.html', bookings=bookings, vacant_rooms=vacant_rooms)

@bookings_bp.route('/bookings', methods=['POST'])
def handle_booking():
    # Gather form data
    guest_id = request.form.get('guest_id')
    room_id = request.form.get('room_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Basic validation
    if not all([guest_id, room_id, start_date, end_date]):
        flash('All fields are required', 'error')
        return redirect(url_for('bookings.bookings_page'))

    # Create booking
    try:
        create_booking(guest_id, room_id, start_date, end_date)
        flash('Booking added successfully! Room status set to Reserved.', 'success')
    except Exception as e:
        flash(f"Error creating booking: {str(e)}", 'error')

    return redirect(url_for('bookings.bookings_page'))

@bookings_bp.route('/bookings/search-guests', methods=['GET'])
def search_guests_route():
    query = request.args.get('q', '')
    if query:
        guests = search_guests(query)
        return jsonify(guests)
    return jsonify([])