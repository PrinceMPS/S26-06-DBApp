from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.bookings_model import get_all_bookings, create_booking_with_payment, update_booking_db, delete_booking_db, \
    get_booking_by_id, get_booking_total_amount_for_new

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
    return render_template('bookings.html', bookings=bookings, editing=form_data)

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

    # Gather form data
    guest_id = request.form.get('guest_id')
    room_id = request.form.get('room_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    amount_paid = request.form.get('amount_paid')
    payment_method = request.form.get('payment_method')

    form_data = {
        'guest_id': guest_id,
        'room_id': room_id,
        'start_date': start_date,
        'end_date': end_date,
        'amount_paid': amount_paid,
        'payment_method': payment_method
    }

    # Handle deletion
    if action == 'delete':
        try:
            delete_booking_db(booking_id)
            flash('Booking deleted successfully! Room status updated to Vacant.', 'success')
        except Exception as e:
            flash(f'Error deleting booking: {str(e)}', 'error')
        return redirect(url_for('bookings.bookings_page'))

    # Handle "Calculate Total" button
    if action == 'calculate':
        if room_id and start_date and end_date:
            try:
                form_data['total_amount'] = get_booking_total_amount_for_new(room_id, start_date, end_date)
                flash(f"Total amount for this booking: {form_data['total_amount']}", 'info')
            except Exception as e:
                flash(f"Cannot calculate total. Check room and dates: {str(e)}", 'error')
        else:
            flash("Please enter room, start date, and end date to calculate total.", 'error')
        return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data)

    # Handle saving (Add/Update)
    if action == 'save':
        # Basic validation
        if not all([guest_id, room_id, start_date, end_date, amount_paid, payment_method]):
            flash('All fields are required', 'error')
            return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data)

        # Calculate total_amount for validation
        try:
            total_amount = get_booking_total_amount_for_new(room_id, start_date, end_date)
            form_data['total_amount'] = total_amount
        except Exception as e:
            flash(f"Cannot calculate total: {str(e)}", 'error')
            return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data)

        # Validate amount paid
        try:
            if float(amount_paid) != float(total_amount):
                flash(f"Amount paid ({amount_paid}) does not match total ({total_amount})", 'error')
                return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data)
        except ValueError:
            flash("Invalid amount paid", 'error')
            return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data)

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
                create_booking_with_payment(guest_id, room_id, start_date, end_date, amount_paid, payment_method)
                flash('Booking added and payment recorded successfully! Room status set to Reserved.', 'success')
        except Exception as e:
            flash(f"Error saving booking: {str(e)}", 'error')
            return render_template('bookings.html', bookings=get_all_bookings(), editing=form_data)

    return redirect(url_for('bookings.bookings_page'))