from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.payments_model import get_all_payments, create_payment,get_booking_total_amount,get_pending_bookings_with_amount,search_pending_bookings_by_booking_id


payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/payments', methods=['GET', 'POST'])
def payments_page():

    # pending bookings
    pending_bookings = get_pending_bookings_with_amount()


    # add payment
    if request.method == 'POST' and request.form.get('action') == 'add_payment':
        try:
            create_payment(request.form)
            flash("Payment added successfully!", "success")
        except Exception as e:
            flash(f"Error adding payment: {str(e)}", "error")
        return redirect(url_for('payments.payments_page'))

    # succesful payments
    payments = get_all_payments()
    for p in payments:
        if hasattr(p['payment_datetime'], "strftime"):
            p['payment_datetime'] = p['payment_datetime'].strftime('%Y-%m-%d %H:%M:%S')

    return render_template(
        'payments.html',
        pending_bookings=pending_bookings,
        payments=payments
    )
@payments_bp.route('/payments/search-pending')
def search_pending():
    query = request.args.get('q', '')
    if query:
        results = search_pending_bookings_by_booking_id(query)
        return jsonify(results)
    return jsonify([])
