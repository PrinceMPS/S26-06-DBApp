from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.employees_model import (
    get_all_employees,
    get_employee_by_id,
    add_employee_db,
    update_employee_db,
    delete_employee_db,
    get_employee_full_details
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
    employee_id = int(employee_id) if employee_id else None

    if action == 'delete':
        if delete_employee_db(employee_id):
            flash('Employee deleted successfully!', 'success')
        else:
            flash('Cannot delete employee: deletion failed due to connection to other records.', 'error')
    else:
        # Handle add/update
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        emp_position = request.form.get('emp_position')
        emp_status = request.form.get('emp_status', 'Active')  # default to Active

        try:
            if employee_id:  # Update existing employee
                update_employee_db(employee_id, first_name, last_name, emp_position, emp_status)
                flash('Employee updated successfully!', 'success')
            else:  # Add new employee
                add_employee_db(first_name, last_name, emp_position, emp_status)
                flash('Employee added successfully!', 'success')
        except Exception as e:
            flash(f'Error saving employee: {str(e)}', 'error')

    return redirect(url_for('employees.employees_page'))


@employees_bp.route('/employees/details/<int:employee_id>')
def employee_details(employee_id):
    employee, checkins_handled, checkouts_handled, items_received, items_issued = get_employee_full_details(employee_id)

    return render_template(
        'employee_details.html',  # separate template for clarity
        employee=employee,
        checkins_handled=checkins_handled,
        checkouts_handled=checkouts_handled,
        items_received = items_received,
        items_issued = items_issued
    )
