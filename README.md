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
- Update the `config.py` file with your database credentials:
  ```python
  DB_CONFIG = {
      "host": "localhost",
      "user": "your_username",
      "password": "your_password",
      "database": "hotel_management"
  }
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
│   ├── guests_controller.py
│   ├── rooms_controller.py
│   ├── employees_controller.py
│   ├── housekeeping_controller.py
│   ├── payments_controller.py
│   ├── gueststay_controller.py
│   └── dashboard_controller.py
├── models/              # Database models and business logic
│   ├── bookings_model.py
│   ├── guests_model.py
│   ├── rooms_model.py
│   ├── employees_model.py
│   ├── housekeeping_model.py
│   ├── payments_model.py
│   ├── gueststay_model.py
│   └── dashboard_model.py
├── templates/           # HTML views
│   ├── bookings/
│   ├── guests/
│   ├── rooms/
│   ├── employees/
│   ├── housekeeping/
│   ├── payments/
│   ├── gueststay/
│   ├── reports/
│   └── dashboard/
├── config.py            # Database configuration
├── app.py              # Flask application entry point
└── requirements.txt    # Python dependencies
```

