from flask import Flask
from controllers.bookings_controller import bookings_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.employees_controller import employees_bp
from controllers.rooms_controller import rooms_bp
from controllers.payment_controller import payments_bp
from controllers.guests_controller import guests_bp

app = Flask(__name__, instance_relative_config=True)
# Set a secret key for sessions (flash messages require this)
app.secret_key = 'secret_key'
app.config.from_pyfile('config.py', silent=False)
app.register_blueprint(dashboard_bp)
# Register blueprint
app.register_blueprint(bookings_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(guests_bp)

if __name__ == '__main__':
    app.run(debug=True)
