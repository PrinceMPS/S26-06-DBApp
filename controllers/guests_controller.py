from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.guests_model import get_all_guests, get_guest_by_id, add_guest_db, update_guest_db, delete_guest_db

guests_bp = Blueprint('guests', __name__)

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