from flask import Blueprint, render_template, request
from models.guest_stay_report_model import get_guest_stay_report

guest_stay_report_bp = Blueprint('guest_stay_report', __name__, url_prefix='/reports')

@guest_stay_report_bp.route('/guest-stay', methods=['GET', 'POST'])
def guest_stay_report():
    guest_stays = []
    total_nights_sum = 0
    total_spending_sum = 0
    selected_month = None
    selected_year = None
    
    # Month names for display
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    if request.method == 'POST':
        selected_month = int(request.form.get('month'))
        selected_year = int(request.form.get('year'))
        
        try:
            guest_stays, total_nights_sum, total_spending_sum = get_guest_stay_report(
                selected_month, selected_year
            )
        except Exception as e:
            # Handle any errors in the report generation
            print(f"Error generating guest stay report: {e}")
    
    # Set default values for first load
    if not selected_year:
        from datetime import datetime
        current_date = datetime.now()
        selected_month = current_date.month
        selected_year = current_date.year
    
    return render_template(
        'reports/guest_stay_report.html',
        guest_stays=guest_stays,
        total_nights_sum=total_nights_sum,
        total_spending_sum=total_spending_sum,
        selected_month=selected_month,
        selected_year=selected_year,
        month_names=month_names
    )