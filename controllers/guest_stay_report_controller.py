from flask import Blueprint, render_template, request
from models.guest_stay_report_model import get_guest_stay_report_month, get_guest_stay_report_year

guest_stay_report_bp = Blueprint('guest_stay_report', __name__, url_prefix='/reports')

@guest_stay_report_bp.route('/guest-stay', methods=['GET', 'POST'])
def guest_stay_report():
    guest_stays = []
    total_nights_sum = 0
    total_spending_sum = 0
    nationality_counts = {}
    selected_month = None
    selected_year = None
    report_type = None
    sort_by = request.args.get('sort_by', 'total_spending')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Month names for display
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    if request.method == 'POST':
        report_type = request.form.get('report_type')  # "month" or "year"
        selected_year = int(request.form.get('year'))
        
        if report_type == 'month':
            selected_month = int(request.form.get('month'))
            try:
                guest_stays, total_nights_sum, total_spending_sum, nationality_counts = get_guest_stay_report_month(
                    selected_month, selected_year
                )
            except Exception as e:
                print(f"Error generating monthly guest stay report: {e}")
        
        elif report_type == 'year':
            try:
                guest_stays, total_nights_sum, total_spending_sum, nationality_counts = get_guest_stay_report_year(
                    selected_year
                )
            except Exception as e:
                print(f"Error generating yearly guest stay report: {e}")
    
    # Set default values for first load
    if not selected_year:
        from datetime import datetime
        current_date = datetime.now()
        selected_month = current_date.month
        selected_year = current_date.year
    
    # Apply sorting
    if guest_stays:
        reverse = sort_order == 'desc'
        if sort_by == 'guest_name':
            guest_stays.sort(key=lambda x: f"{x['first_name']} {x['last_name']}".lower(), reverse=reverse)
        elif sort_by == 'nationality':
            guest_stays.sort(key=lambda x: x.get('nationality', '').lower(), reverse=reverse)
        elif sort_by == 'total_stays':
            guest_stays.sort(key=lambda x: x.get('total_stays', 0), reverse=reverse)
        elif sort_by == 'total_nights':
            guest_stays.sort(key=lambda x: x.get('total_nights', 0), reverse=reverse)
        elif sort_by == 'total_spending':
            guest_stays.sort(key=lambda x: x.get('total_spending', 0), reverse=reverse)
        else:  # default sort by guest_id
            guest_stays.sort(key=lambda x: x.get('guest_id', 0), reverse=reverse)
    
return render_template(
    'reports/guest_stay_report.html',
    guest_stays=guest_stays,
    total_nights_sum=total_nights_sum,
    total_spending_sum=total_spending_sum,
    nationality_counts=nationality_stats, 
    selected_month=selected_month,
    selected_year=selected_year,
    report_type=report_type,
    month_names=month_names,
    sort_by=sort_by,
    sort_order=sort_order
)