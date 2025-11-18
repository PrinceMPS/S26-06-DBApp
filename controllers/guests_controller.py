from flask import Blueprint, render_template, request, redirect, url_for, flash
import re
from models.guests_model import get_all_guests, get_guest_by_id, add_guest_db, update_guest_db, delete_guest_db, get_guest_full_details

guests_bp = Blueprint('guests', __name__)

def validate_contact_number(contact_number):
    """
    Validate contact number format:
    - Starts with '09' followed by 9 digits (11 digits total) OR
    - Starts with '+' followed by country code and number
    """
    # Pattern for Philippine numbers: 09XXXXXXXXX (11 digits)
    ph_pattern = r'^09\d{9}$'
    
    # Pattern for international numbers: + followed by 1-15 digits
    intl_pattern = r'^\+\d{1,15}$'
    
    # Remove any spaces, dashes, or parentheses
    clean_number = re.sub(r'[\s\-\(\)]', '', contact_number)
    
    return bool(re.match(ph_pattern, clean_number) or re.match(intl_pattern, clean_number))

def validate_email(email):
    """
    Validate email address format
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

@guests_bp.route('/guests', methods=['GET'])
def guests_page():
    guests = get_all_guests()
    return render_template('guests.html', guests=guests)

@guests_bp.route('/guests/edit/<int:guest_id>')
def edit_guest(guest_id):
    guest = get_guest_by_id(guest_id)
    guests = get_all_guests()
    return render_template('guests.html', guests=guests, editing=guest)

@guests_bp.route('/guests', methods=['POST'])
def handle_guest():
    action = request.form.get('action', 'save')
    guest_id = request.form.get('guest_id')
    
    if action == 'delete':
        # Handle delete
        try:
            delete_guest_db(guest_id)
            flash('Guest deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting guest: {str(e)}', 'error')
    else:
        # Handle add/update
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email_address = request.form.get('email_address')
        nationality = request.form.get('nationality')
        
        # Basic validation
        if not all([first_name, last_name, contact_number, email_address, nationality]):
            flash('All fields are required', 'error')
            return redirect(url_for('guests.guests_page'))
        
        # Contact number validation
        if not validate_contact_number(contact_number):
            flash('Invalid contact number format. Use 09XXXXXXXXX or +CountryCodeNumber', 'error')
            return redirect(url_for('guests.guests_page'))
        
        # Email validation
        if not validate_email(email_address):
            flash('Invalid email address format', 'error')
            return redirect(url_for('guests.guests_page'))
        
        try:
            if guest_id:  # Update existing guest
                update_guest_db(guest_id, first_name, last_name, contact_number, email_address, nationality)
                flash('Guest updated successfully!', 'success')
            else:  # Add new guest
                add_guest_db(first_name, last_name, contact_number, email_address, nationality)
                flash('Guest added successfully!', 'success')
        except Exception as e:
            flash(f'Error saving guest: {str(e)}', 'error')
    
    return redirect(url_for('guests.guests_page'))

@guests_bp.route('/guests/details/<int:guest_id>')
def guest_details(guest_id):
    guest, bookings, guest_stays = get_guest_full_details(guest_id)
    
    return render_template(
        'guest_details.html',
        guest=guest,
        bookings=bookings,
        guest_stays=guest_stays
    )