# controllers/dashboard_controller.py
from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def show_dashboard():
    # Temporary filler values for testing the dashboard UI
    total_guests = 20
    occupied_rooms = 15
    total_rooms = 30
    total_employees = 10
    total_revenue = 50000.00

    return render_template('dashboard.html',
                           total_guests=total_guests,
                           occupied_rooms=occupied_rooms,
                           total_rooms=total_rooms,
                           total_employees=total_employees,
                           total_revenue=total_revenue)
