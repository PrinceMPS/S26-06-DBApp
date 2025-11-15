from flask import Blueprint, render_template
from models.dashboard_model import get_total_guests, get_room_occupancy, get_total_employees, get_todays_revenue

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard_page():
    total_guests = get_total_guests()
    total_rooms, occupied_rooms = get_room_occupancy()
    total_employees = get_total_employees()
    total_revenue = get_todays_revenue()
    
    return render_template('dashboard.html', 
                         total_guests=total_guests,
                         total_rooms=total_rooms,
                         occupied_rooms=occupied_rooms,
                         total_employees=total_employees,
                         total_revenue=total_revenue)


