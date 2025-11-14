from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.gueststay_model import (
    search_booking,
    get_frontdesk_employees,
    check_in_guest,
    check_out_guest,
    get_booking_details
)
from datetime import datetime, date

gueststay_bp = Blueprint('gueststay', __name__)


@gueststay_bp.route('/gueststay', methods=['GET'])
def gueststay_page():
    """
    Display the guest stay management page
    """
    employees = get_frontdesk_employees()
    return render_template('gueststay.html', employees=employees)


@gueststay_bp.route('/gueststay/search', methods=['POST'])
def search_gueststay():
    """
    Search for bookings based on booking_id, guest_id, or date
    """
    booking_id = request.form.get('booking_id', '').strip()
    guest_id = request.form.get('guest_id', '').strip()
    search_date = request.form.get('search_date', '').strip()
    
    # Convert empty strings to None
    booking_id = int(booking_id) if booking_id else None
    guest_id = int(guest_id) if guest_id else None
    search_date = search_date if search_date else None
    
    # Validate that at least one search criteria is provided
    if not booking_id and not guest_id and not search_date:
        flash('Please provide at least one search criteria (Booking ID, Guest ID, or Date)', 'error')
        employees = get_frontdesk_employees()
        return render_template('gueststay.html', employees=employees)
    
    # Search for bookings
    results = search_booking(booking_id, guest_id, search_date)
    
    if not results:
        flash('No booking found matching the search criteria', 'error')
        employees = get_frontdesk_employees()
        return render_template('gueststay.html', employees=employees)
    
    # If single booking found, display it with action options
    # If multiple bookings found, display list
    employees = get_frontdesk_employees()
    current_date = date.today()
    
    # Determine action for each booking
    for booking in results:
        booking['action'] = determine_action(booking, search_date or str(current_date))
    
    return render_template('gueststay.html', 
                         bookings=results, 
                         employees=employees,
                         search_date=search_date or str(current_date))


def determine_action(booking, check_date):
    """
    Determine what action can be taken for a booking based on date and status
    """
    if isinstance(check_date, str):
        check_date = datetime.strptime(check_date, '%Y-%m-%d').date()
    
    start_date = booking['start_date']
    end_date = booking['end_date']
    
    # Check if already checked in
    if booking['check_in_time_date']:
        # Already checked in, check if checked out
        if booking['actual_check_out_time_date']:
            return 'completed'  # Already checked out
        else:
            # Can check out if date >= start_date
            if check_date >= start_date:
                return 'checkout'
            else:
                return 'checked_in'  # Checked in but not time to check out yet
    else:
        # Not checked in yet
        if check_date == start_date:
            return 'checkin'  # Can check in on start date
        elif check_date > start_date and check_date <= end_date:
            return 'late_checkin'  # Late check-in
        elif check_date < start_date:
            return 'early'  # Too early to check in
        else:
            return 'expired'  # Booking date has passed


@gueststay_bp.route('/gueststay/checkin', methods=['POST'])
def checkin():
    """
    Process guest check-in
    """
    booking_id = request.form.get('booking_id')
    employee_id = request.form.get('employee_id')
    remarks = request.form.get('remarks', '').strip()
    
    if not booking_id or not employee_id:
        flash('Booking ID and Employee are required for check-in', 'error')
        return redirect(url_for('gueststay.gueststay_page'))
    
    try:
        # Get booking details to set expected checkout time
        booking = get_booking_details(booking_id)
        
        if not booking:
            flash('Booking not found', 'error')
            return redirect(url_for('gueststay.gueststay_page'))
        
        # Set check-in time to current time
        check_in_time = datetime.now()
        
        # Set expected checkout time to end_date at 12:00 PM
        expected_checkout = datetime.combine(booking['end_date'], datetime.strptime('12:00', '%H:%M').time())
        
        # Perform check-in
        transaction_id = check_in_guest(
            booking_id=booking_id,
            employee_id=employee_id,
            check_in_time=check_in_time,
            expected_checkout_time=expected_checkout,
            remarks=remarks
        )
        
        flash(f'Guest checked in successfully! Transaction ID: {transaction_id}', 'success')
        
    except Exception as e:
        flash(f'Error during check-in: {str(e)}', 'error')
    
    return redirect(url_for('gueststay.gueststay_page'))


@gueststay_bp.route('/gueststay/checkout', methods=['POST'])
def checkout():
    """
    Process guest check-out
    """
    booking_id = request.form.get('booking_id')
    remarks = request.form.get('remarks', '').strip()
    
    if not booking_id:
        flash('Booking ID is required for check-out', 'error')
        return redirect(url_for('gueststay.gueststay_page'))
    
    try:
        # Set checkout time to current time
        checkout_time = datetime.now()
        
        # Perform check-out
        check_out_guest(
            booking_id=booking_id,
            actual_checkout_time=checkout_time,
            remarks=remarks
        )
        
        flash('Guest checked out successfully!', 'success')
        
    except Exception as e:
        flash(f'Error during check-out: {str(e)}', 'error')
    
    return redirect(url_for('gueststay.gueststay_page'))
