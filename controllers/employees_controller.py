from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.employees_model import (
    get_all_employees,
    get_employee_by_id,
    add_employee_db,
    update_employee_db,
    delete_employee_db
)

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/employees', methods=['GET'])
def employees_page():
    employees = get_all_employees()
    return render_template('employees.html', employees=employees)

@employees_bp.route('/employees/edit/<int:employee_id>')
def edit_employee(employee_id):
    employee = get_employee_by_id(employee_id)
    employees = get_all_employees()
    return render_template('employees.html', employees=employees, editing=employee)

@employees_bp.route('/employees', methods=['POST'])
def handle_employee():
    action = request.form.get('action', 'save')
    employee_id = request.form.get('employee_id')

    if action == 'delete':
        # Handle delete
        try:
            delete_employee_db(employee_id)
            flash('Employee deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting employee: {str(e)}', 'error')
    else:
        # Handle add/update
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        emp_position = request.form.get('emp_position')
        shift = request.form.get('shift')
        emp_status = request.form.get('emp_status', 'Active')  # default to Active

        try:
            if employee_id:  # Update existing employee
                update_employee_db(employee_id, first_name, last_name, emp_position, shift, emp_status)
                flash('Employee updated successfully!', 'success')
            else:  # Add new employee
                add_employee_db(first_name, last_name, emp_position, shift, emp_status)
                flash('Employee added successfully!', 'success')
        except Exception as e:
            flash(f'Error saving employee: {str(e)}', 'error')

    return redirect(url_for('employees.employees_page'))
