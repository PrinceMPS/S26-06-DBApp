# Hotel Management Simulation
CCINFOM-S26-06 DBApp for Term 1, 2025-2026


## Project Overview

A comprehensive Hotel Management System built with Flask (Python) and MySQL that streamlines hotel operations including room reservations, guest management, housekeeping, and payment processing.


**Key Features:**  
✅ Room reservation system with real-time availability  
✅ Guest management and check-in/check-out processing  
✅ Housekeeping items tracking and inventory management  
✅ Payment processing and revenue tracking  
✅ Comprehensive reporting and analytics  
✅ Real-time dashboard with occupancy and revenue metrics  



## How to use

## Prerequisites

Before running the Hotel Management System, make sure the following are installed on your machine:

1. **Python 3.10+**  
   - [Download Python](https://www.python.org/downloads/) and install it.  
   - Verify installation:
     ```bash
     python --version
     ```

2. **pip (Python package manager)**  
   - Usually comes with Python.  
   - Verify installation:
     ```bash
     pip --version
     ```

3. **MySQL**  
   - [Download and install MySQL](https://dev.mysql.com/downloads/).  
   - Make sure the MySQL server is running and you know your username/password.  
   - Verify installation:
     ```bash
     mysql --version
     ```

## Installation & Setup

1. **Clone the repository**  
```
git clone https://github.com/PrinceMPS/S26-06-DBApp.git
cd S26-06-DBAPP
```

2. **Install Python dependencies**  
   - Navigate to your project directory and install all required Python packages listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - This will install packages such as `Flask`, `PyMySQL`, and any other dependencies your project uses.

3. **Database Configuration** 

- Create a MySQL database named `hotel_management`
  ```sql
  CREATE DATABASE hotel_management;
  ```
create a file called `config.py` file with your database credentials:
  ```python
# config.py
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "hotel_management"
}

# Add this simple secret key (no need to change)
SECRET_KEY = 'your-secret-key-here-12345'
  ```
- Run the Application
  ```bash
  python app.py
  ```
- Access the Application
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```


## Project Architecture
The application follows the **Model-View-Controller (MVC)** pattern:

### Directory Structure
```text
S26-06-DBApp/
├── controllers/          # Application controllers
│   ├── bookings_controller.py
│   ├── dashboard_controller.py
│   ├── employees_controller.py
│   ├── guest_stay_controller.py
│   ├── guests_controller.py
│   ├── gueststay_controller.py
│   ├── hotel_occupancy_report_controller.py
│   ├── hotel_revenue_report_controller.py
│   ├── housekeeping_controller.py
│   ├── index_controller.py
│   ├── items_usage_report_controller.py
│   ├── payment_controller.py
│   ├── reports_controller.py
│   ├── room_details_controller.py
│   └── rooms_controller.py
│
├── database/            # SQL Database
│   └── hotel_management.sql
│
├── instance/            # Flask instance folder (config per deployment)
│   └── config.py
│
├── models/              # Database models and business logic
│   ├── bookings_model.py
│   ├── dashboard_model.py
│   ├── employees_model.py
│   ├── guest_stay_model.py
│   ├── guests_model.py
│   ├── gueststay_model.py
│   ├── housekeeping_items_model.py
│   ├── index_model.py
│   ├── items_usage_report_model.py
│   ├── occupancy_report_model.py
│   ├── payment_model.py
│   ├── reports_model.py
│   ├── revenue_report_model.py
│   ├── room_details_model.py
│   └── rooms_model.py
│
├── templates/           # HTML views
│   ├── reports/
│   │   ├── guest_stay_report.html
│   │   ├── hotel_occupancy.html
│   │   ├── hotel_revenue.html
│   │   ├── index.html
│   │   └── items_usage_report.html
│   ├── bookings.html
│   ├── dashboard.html
│   ├── employee_details.html
│   ├── employees.html
│   ├── guest_details.html
│   ├── guests.html
│   ├── gueststay.html
│   ├── housekeeping_items.html
│   ├── payment.html
│   ├── room_details.html
│   └── rooms.html
│
├── app.py              # Flask application entry point: initializes app, blueprints, and server
├── config.py           # Global configuration (DB URI, secret keys, settings)
├── db.py               # Database connection helper / wrapper functions
├── README.md           # Project overview and instructions
└── requirements.txt    # Python dependencies (Flask, SQLAlchemy, etc.)
```

