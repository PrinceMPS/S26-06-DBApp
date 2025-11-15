from flask import Blueprint, render_template, request, flash
from models.revenue_report_model  import get_hotel_revenue_report_month, get_hotel_revenue_report_year

hotel_revenue_bp = Blueprint('hotel_revenue', __name__, url_prefix='/reports')


@hotel_revenue_bp.route('/hotel-revenue', methods=['GET', 'POST'])
def hotel_revenue_report():
    report_data = []
    grand_total = 0
    selected_year = None
    selected_month = None

    if request.method == 'POST':
        report_type = request.form.get('report_type')  # "month" or "year"
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')

        if report_type == 'month':
            if selected_year and selected_month:
                report_data, grand_total = get_hotel_revenue_report_month(int(selected_year), int(selected_month))
            else:
                flash("Please select both month and year for monthly report.", "error")

        elif report_type == 'year':
            if selected_year:
                report_data, grand_total = get_hotel_revenue_report_year(int(selected_year))
            else:
                flash("Please select a year for yearly report.", "error")

    return render_template(
        'reports/hotel_revenue.html',
        report_data=report_data,
        grand_total=grand_total,
        selected_year=selected_year,
        selected_month=selected_month
    )
