from flask import Blueprint, render_template, request, flash
from models.occupancy_report_model import get_hotel_occupancy_month

hotel_occupancy_bp = Blueprint('hotel_occupancy', __name__, url_prefix='/reports')


@hotel_occupancy_bp.route('/hotel-occupancy', methods=['GET', 'POST'])
def hotel_occupancy_report():
    report = None
    selected_year = None
    selected_month = None

    if request.method == 'POST':
        try:
            selected_year = int(request.form.get('year'))
            selected_month = int(request.form.get('month'))
            report = get_hotel_occupancy_month(selected_year, selected_month)
        except Exception as e:
            flash(f"Error generating report: {e}", 'error')

    return render_template(
        'reports/hotel_occupancy.html',
        report=report,
        selected_year=selected_year,
        selected_month=selected_month
    )
