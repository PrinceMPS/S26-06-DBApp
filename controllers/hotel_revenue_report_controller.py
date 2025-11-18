from flask import Blueprint, render_template, request, flash
from models.revenue_report_model  import get_hotel_revenue_report_month, get_hotel_revenue_report_year

hotel_revenue_bp = Blueprint('hotel_revenue', __name__, url_prefix='/reports')


@hotel_revenue_bp.route('/hotel-revenue', methods=['GET', 'POST'])
def hotel_revenue_report():
    report_data = []
    grand_total = 0
    monthly_summary = []
    selected_year = None
    selected_month = None
    report_type = None

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        selected_year = int(request.form.get('year')) if request.form.get('year') else None
        selected_month = int(request.form.get('month')) if request.form.get('month') else None


        if report_type == 'month':
            if selected_year and selected_month:
                report_data, grand_total, highest_monthly= get_hotel_revenue_report_month(int(selected_year), int(selected_month))
            else:
                flash("Please select both month and year for monthly report.", "error")

        elif report_type == 'year':
            if selected_year:
                report_data, grand_total, monthly_summary, highest_yearly = get_hotel_revenue_report_year(int(selected_year))
            else:
                flash("Please select a year for yearly report.", "error")

    return render_template(
        'reports/hotel_revenue.html',
        report_data=report_data,
        grand_total=grand_total,
        monthly_summary=monthly_summary,
        selected_year=selected_year,
        selected_month=selected_month,
        month_names=month_names,
        report_type = report_type,
        highest_monthly = highest_monthly if report_type == 'month' else None,
        highest_yearly = highest_yearly if report_type == 'year' else None,


    )
