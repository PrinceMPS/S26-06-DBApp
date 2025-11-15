from flask import Flask
from controllers.dashboard_controller import dashboard_bp
from controllers.bookings_controller import bookings_bp
from controllers.employees_controller import employees_bp
from controllers.rooms_controller import rooms_bp
from controllers.payment_controller import payments_bp
from controllers.guests_controller import guests_bp
from controllers.gueststay_controller import gueststay_bp
from controllers.housekeeping_items_controller import housekeeping_bp
from controllers.index_controller import reports_bp
from controllers.hotel_revenue_report_controller import hotel_revenue_bp
app = Flask(__name__, instance_relative_config=True)
# Set a secret key for sessions (flash messages require this)
app.secret_key = 'secret_key'
app.config.from_pyfile('config.py', silent=False)

# Register blueprint
app.register_blueprint(dashboard_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(guests_bp)
app.register_blueprint(gueststay_bp)
app.register_blueprint(housekeeping_bp)
app.register_blueprint(reports_bp)

app.register_blueprint(hotel_revenue_bp)


if __name__ == '__main__':
    app.run(debug=True)
