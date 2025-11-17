from flask import Blueprint, render_template, request, flash
from models.items_usage_report_model import (
    get_items_usage_report_month, 
    get_items_usage_report_year,
    get_all_housekeeping_items
)

items_usage_report_bp = Blueprint('items_usage_report', __name__, url_prefix='/reports')


@items_usage_report_bp.route('/items-usage/', methods=['GET', 'POST'])
def items_usage_report_page():
    report_data = []
    grand_total = 0
    total_quantity = 0
    selected_year = None
    selected_month = None
    selected_item = None
    selected_item_name = None

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Get all items for dropdown
    all_items = get_all_housekeeping_items()
    
    if request.method == 'POST':
        report_type = request.form.get('report_type')  # "month" or "year"
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        selected_item = request.form.get('item_id')  # Can be empty for all items

        # Get selected item name for display
        if selected_item:
            for item in all_items:
                if str(item['housekeeping_item_id']) == selected_item:
                    selected_item_name = item['item_name']
                    break

        if report_type == 'month':
            if selected_year and selected_month:
                report_data, grand_total, total_quantity = get_items_usage_report_month(
                    int(selected_year), 
                    int(selected_month), 
                    int(selected_item) if selected_item else None
                )
            else:
                flash("Please select both month and year for monthly report.", "error")

        elif report_type == 'year':
            if selected_year:
                report_data, grand_total, total_quantity = get_items_usage_report_year(
                    int(selected_year), 
                    int(selected_item) if selected_item else None
                )
            else:
                flash("Please select a year for yearly report.", "error")

    return render_template(
        'reports/items_usage_report.html',
        report_data=report_data,
        grand_total=grand_total,
        total_quantity=total_quantity,
        selected_year=selected_year,
        selected_month=selected_month,
        selected_item=selected_item,
        selected_item_name=selected_item_name,
        month_names=month_names,
        all_items=all_items
    )