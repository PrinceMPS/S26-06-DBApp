from flask import Blueprint, render_template, request, redirect, url_for
from models.bookings_model import get_all_bookings, add_booking

bookings_bp = Blueprint('bookings', __name__, template_folder='../templates')


@bookings_bp.route('/bookings', methods=['GET', 'POST'])
def bookings_list():
    if request.method == 'POST':
        # Read form data
        guest_id = request.form.get('guest_id')
        room_id = request.form.get('room_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Insert into database
        add_booking(guest_id, room_id, start_date, end_date)

        # Redirect to avoid form resubmission
        return redirect(url_for('bookings.bookings_list'))

    # Handle GET: display all bookings
    bookings = get_all_bookings()

    # Convert datetime/date fields to string
    for b in bookings:
        for key, value in b.items():
            if hasattr(value, "strftime"):  # if it's a date/datetime object
                b[key] = value.strftime('%Y-%m-%d')

    return render_template('bookings.html', bookings=bookings)
