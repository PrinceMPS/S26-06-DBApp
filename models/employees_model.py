from db import get_db_connection

def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            employee_id,
            first_name,
            last_name,
            emp_position,
            shift,
            emp_status
        FROM employee
        ORDER BY last_name ASC
    """)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return employees

def get_employee_by_id(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    return employee

def add_employee_db(first_name, last_name, emp_position, shift, emp_status='Active'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employee (first_name, last_name, emp_position, shift, emp_status)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, last_name, emp_position, shift, emp_status))
    conn.commit()
    cursor.close()
    conn.close()

def update_employee_db(employee_id, first_name, last_name, emp_position, shift, emp_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employee
        SET first_name = %s, last_name = %s, emp_position = %s, shift = %s, emp_status = %s
        WHERE employee_id = %s
    """, (first_name, last_name, emp_position, shift, emp_status, employee_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_employee_db(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE employee_id = %s", (employee_id,))
    conn.commit()
    cursor.close()
    conn.close()
