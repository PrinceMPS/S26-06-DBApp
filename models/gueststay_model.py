from db import get_db_connection
from datetime import datetime, date

def search_booking(booking_id=None, guest_id=None, search_date=None):
    """
    Search for bookings based on booking_id, guest_id, or date
    Returns booking information with guest stay status
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            b.booking_id,
            b.guest_id,
            b.room_id,
            b.booking_date,
            b.start_date,
            b.end_date,
            g.first_name AS guest_first_name,
            g.last_name AS guest_last_name,
            g.contact_number,
            g.email_address,
            r.room_id,
            rt.type_name AS room_type,
            rt.rate_per_type,
            gs.transaction_id,
            gs.employee_id,
            gs.check_in_time_date,
            gs.expected_check_out_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN employee e ON gs.employee_id = e.employee_id
        WHERE 1=1
    """
    
    params = []
    
    if booking_id:
        query += " AND b.booking_id = %s"
        params.append(booking_id)
    
    if guest_id:
        query += " AND b.guest_id = %s"
        params.append(guest_id)
    
    if search_date:
        query += " AND %s BETWEEN b.start_date AND b.end_date"
        params.append(search_date)
    
    query += " ORDER BY b.booking_date DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results


def get_frontdesk_employees():
    """
    Get all active frontdesk and admin employees
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            employee_id,
            CONCAT(first_name, ' ', last_name) AS employee_name,
            emp_position
        FROM employee
        WHERE emp_position IN ('frontdesk', 'admin')
        AND emp_status = 'Active'
        ORDER BY first_name, last_name
    """
    
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return employees


def check_in_guest(booking_id, employee_id, check_in_time, expected_checkout_time, remarks=None):
    """
    Check in a guest for their booking
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if guest stay already exists
        cursor.execute("SELECT transaction_id FROM GuestStay WHERE booking_id = %s", (booking_id,))
        existing = cursor.fetchone()
        
        if existing:
            raise Exception("Guest is already checked in for this booking")
        
        # Insert new guest stay record
        query = """
            INSERT INTO GuestStay 
            (booking_id, employee_id, check_in_time_date, expected_check_out_time_date, remarks)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (booking_id, employee_id, check_in_time, expected_checkout_time, remarks))
        
        # Update room status to Booked
        cursor.execute("""
            UPDATE room r
            JOIN booking b ON r.room_id = b.room_id
            SET r.availability_status = 'Booked'
            WHERE b.booking_id = %s
        """, (booking_id,))
        
        conn.commit()
        transaction_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return transaction_id
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise e


def check_out_guest(booking_id, employee_id, actual_checkout_time, remarks=None):
    """
    Check out a guest from their booking
    Note: employee_id is for the employee facilitating checkout (may be different from check-in employee)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if guest stay exists and guest is checked in
        cursor.execute("""
            SELECT transaction_id, actual_check_out_time_date 
            FROM GuestStay 
            WHERE booking_id = %s
        """, (booking_id,))
        
        guest_stay = cursor.fetchone()
        
        if not guest_stay:
            raise Exception("Guest is not checked in for this booking")
        
        if guest_stay[1] is not None:  # actual_check_out_time_date
            raise Exception("Guest has already checked out")
        
        # Update guest stay with checkout time
        # Note: We keep the original employee_id (who checked in) and just update checkout time
        # If you want to track checkout employee separately, you'd need to add a checkout_employee_id column
        query = """
            UPDATE GuestStay 
            SET actual_check_out_time_date = %s,
                remarks = %s
            WHERE booking_id = %s
        """
        
        cursor.execute(query, (actual_checkout_time, remarks, booking_id))
        
        # Update room status back to Vacant
        cursor.execute("""
            UPDATE room r
            JOIN booking b ON r.room_id = b.room_id
            SET r.availability_status = 'Vacant'
            WHERE b.booking_id = %s
        """, (booking_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise e


def get_booking_details(booking_id):
    """
    Get detailed information about a specific booking
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            b.booking_id,
            b.guest_id,
            b.room_id,
            b.booking_date,
            b.start_date,
            b.end_date,
            g.first_name AS guest_first_name,
            g.last_name AS guest_last_name,
            g.contact_number,
            g.email_address,
            g.nationality,
            rt.type_name AS room_type,
            rt.rate_per_type,
            rt.capacity,
            gs.transaction_id,
            gs.employee_id,
            gs.check_in_time_date,
            gs.expected_check_out_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            e.emp_position
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN employee e ON gs.employee_id = e.employee_id
        WHERE b.booking_id = %s
    """
    
    cursor.execute(query, (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return booking
