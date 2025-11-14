from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.payments_model import get_all_payments, get_payment_by_id, update_payment_db, delete_payment_db
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

# Display all payments
@payments_bp.route('/payments', methods=['GET'])
def payments_page():
    payments = get_all_payments()
    # Convert datetime to string for display
    for payment in payments:
        for key, value in payment.items():
            if hasattr(value, "strftime"):
                payment[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('payments.html', payments=payments)

# Edit payment form
@payments_bp.route('/payments/edit/<int:payment_id>', methods=['GET'])
def edit_payment(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment:
        # Convert datetime for form display
        for key, value in payment.items():
            if hasattr(value, "strftime"):
                payment[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    payments = get_all_payments()
    # Convert datetime for table display
    for p in payments:
        for key, value in p.items():
            if hasattr(value, "strftime"):
                p[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    return render_template('payments.html', payments=payments, editing=payment)

# Handle update or delete
@payments_bp.route('/payments', methods=['POST'])
def handle_payment():
    action = request.form.get('action', 'save')
    payment_id = request.form.get('payment_id')

    if action == 'delete':
        try:
            delete_payment_db(payment_id)
            flash('Payment deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting payment: {str(e)}', 'error')
    else:
        # Only allow update
        booking_id = request.form.get('booking_id') # shuold this be allowed
        amount_paid = request.form.get('amount_paid')
        payment_method = request.form.get('payment_method')


        try:
            if payment_id:
                update_payment_db(payment_id,booking_id, amount_paid, payment_method)
                flash('Payment updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating payment: {str(e)}', 'error')

    return redirect(url_for('payments.payments_page'))
