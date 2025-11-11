from flask import Blueprint, render_template, request
from models.reports_model import get_total_booked_days_by_room

reports_bp = Blueprint('reports', __name__, template_folder='../templates/admin/reports')

@reports_bp.route('/room-booked-days', methods=['GET', 'POST'])
def room_booked_days_report():
    total_days = None
    if request.method == 'POST':
        room_id = int(request.form.get('room_id'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))

        total_days = get_total_booked_days_by_room(room_id, month, year)

    return render_template('room-booked-days.html', total_days=total_days)
