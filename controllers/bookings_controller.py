from flask import Blueprint, render_template
from models.bookings_model import get_all_bookings

bookings_bp = Blueprint('bookings', __name__, template_folder='../templates')

@bookings_bp.route('/bookings')
def bookings_list():
    bookings = get_all_bookings()

    # Convert datetime/date fields to string
    for b in bookings:
        for key, value in b.items():
            if hasattr(value, "strftime"):  # if it's a date/datetime object
                b[key] = value.strftime('%Y-%m-%d')

    return render_template('bookings.html', bookings=bookings)
