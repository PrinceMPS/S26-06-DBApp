from flask import Blueprint, render_template, request, flash
from models.items_usage_report_model import (
    get_items_usage_report_month, 
    get_items_usage_report_year,
    get_all_housekeeping_items,
    get_yearly_metrics,
    get_available_years,
    get_yearly_monthly_breakdown,
    get_specific_item_yearly_metrics
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
    yearly_metrics = None
    monthly_breakdown = None
    specific_item_metrics = None

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Get all items for dropdown and available years
    all_items = get_all_housekeeping_items()
    available_years = get_available_years()
    
    # Set default selected year to most recent year if available
    default_year = available_years[0] if available_years else None
    
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
                
                # Get monthly breakdown for yearly reports
                monthly_breakdown = get_yearly_monthly_breakdown(
                    int(selected_year), 
                    int(selected_item) if selected_item else None
                )
                
                # Get metrics based on whether specific item is selected
                if selected_item:
                    specific_item_metrics = get_specific_item_yearly_metrics(
                        int(selected_year), 
                        int(selected_item)
                    )
                    # Ensure item_data exists in specific_item_metrics
                    if specific_item_metrics and not specific_item_metrics.get('item_data'):
                        specific_item_metrics['item_data'] = {
                            'total_cost': 0,
                            'total_quantity': 0,
                            'cost_per_unit': 0,
                            'item_name': selected_item_name
                        }
                else:
                    yearly_metrics = get_yearly_metrics(int(selected_year))
                    
            else:
                flash("Please select a year for yearly report.", "error")
    else:
        # For GET requests, set default year
        selected_year = default_year

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
        all_items=all_items,
        yearly_metrics=yearly_metrics,
        monthly_breakdown=monthly_breakdown,
        specific_item_metrics=specific_item_metrics,
        available_years=available_years
    )