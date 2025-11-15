from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.payments_model import get_all_payments


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

