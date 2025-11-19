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
            emp_status
        FROM employee
        ORDER BY employee_id ASC
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

def add_employee_db(first_name, last_name, emp_position, emp_status='Active'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employee (first_name, last_name, emp_position, emp_status)
        VALUES (%s, %s, %s, %s)
    """, (first_name, last_name, emp_position, emp_status))
    conn.commit()
    cursor.close()
    conn.close()

def update_employee_db(employee_id, first_name, last_name, emp_position,  emp_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employee
        SET first_name = %s, last_name = %s, emp_position = %s, emp_status = %s
        WHERE employee_id = %s
    """, (first_name, last_name, emp_position, emp_status, employee_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_employee_db(employee_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE employee_id = %s", (employee_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
    except Exception:
        deleted = False
    finally:
        cursor.close()
        conn.close()
    return deleted

def get_employee_full_details(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Employee basic info
    cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (employee_id,))
    employee = cursor.fetchone()

    # Guests attended by employee check in
    cursor.execute("""
         SELECT 
        CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
        g.guest_id,     
        g.contact_number,
        g.email_address,
        g.nationality,
        gs.check_in_time_date,     
        gs.transaction_id,
        gs.booking_id
    FROM GuestStay gs
    JOIN booking b ON gs.booking_id = b.booking_id
    JOIN guest g ON b.guest_id = g.guest_id
    WHERE gs.checkin_employee_id = %s
    ORDER BY gs.check_in_time_date DESC
    """, (employee_id,))
    checkins_handled = cursor.fetchall()

    # Guests employee checked out
    cursor.execute("""
         SELECT 
        CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
        g.guest_id,     
        g.contact_number,
        g.email_address,
        g.nationality,
        gs.actual_check_out_time_date,    
        gs.transaction_id,
        gs.booking_id
    FROM GuestStay gs
    JOIN booking b ON gs.booking_id = b.booking_id
    JOIN guest g ON b.guest_id = g.guest_id
    WHERE gs.checkout_employee_id = %s
    ORDER BY gs.actual_check_out_time_date DESC
                   """, (employee_id,))
    checkouts_handled = cursor.fetchall()
    # Items issued TO the employee
    cursor.execute("""
                   SELECT h.item_name,
                        h.housekeeping_item_id,
                          i.quantity_issued,
                          i.date_issued,
                           CONCAT(e.first_name, ' ', e.last_name) AS issuer_name
                   FROM housekeeping_item_issuance i
                            JOIN housekeeping_item h ON i.housekeeping_item_id = h.housekeeping_item_id
                            JOIN employee e ON i.issuer_id = e.employee_id
                   WHERE i.employee_id = %s
                   ORDER BY i.date_issued DESC
                   """, (employee_id,))
    items_received = cursor.fetchall()

    # Items issued BY the employee
    cursor.execute("""
                   SELECT h.item_name,
                          h.housekeeping_item_id,
                          i.quantity_issued,
                          i.date_issued,
                          CONCAT(e.first_name, ' ', e.last_name) AS recipient_name
                   FROM housekeeping_item_issuance i
                            JOIN housekeeping_item h ON i.housekeeping_item_id = h.housekeeping_item_id
                            JOIN employee e ON i.employee_id = e.employee_id
                   WHERE i.issuer_id = %s
                   ORDER BY i.date_issued DESC
                   """, (employee_id,))
    items_issued = cursor.fetchall()


    return employee, checkins_handled,checkouts_handled, items_received, items_issued
