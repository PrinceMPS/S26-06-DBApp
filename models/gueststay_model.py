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
            b.payment_status,
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
            gs.checkin_employee_id,
            gs.checkout_employee_id,
            gs.check_in_time_date,
            gs.expected_check_out_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            CONCAT(e_checkin.first_name, ' ', e_checkin.last_name) AS checkin_employee_name,
            CONCAT(e_checkout.first_name, ' ', e_checkout.last_name) AS checkout_employee_name
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN employee e_checkin ON gs.checkin_employee_id = e_checkin.employee_id
        LEFT JOIN employee e_checkout ON gs.checkout_employee_id = e_checkout.employee_id
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
        WHERE emp_position IN ('Front Desk', 'Admin')
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
    Validates payment status before allowing check-in
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
   
    try:
        # Check if guest stay already exists
        cursor.execute("SELECT transaction_id FROM GuestStay WHERE booking_id = %s", (booking_id,))
        existing = cursor.fetchone()
       
        if existing:
            raise Exception("Guest is already checked in for this booking")
       
        # Check payment status - must be 'Paid' before check-in
        cursor.execute("SELECT payment_status FROM booking WHERE booking_id = %s", (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            raise Exception("Booking not found")
        
        if booking['payment_status'] != 'Paid':
            raise Exception("Payment must be completed before check-in. Current status: " + booking['payment_status'])
       
        # Insert new guest stay record with check-in employee
        query = """
            INSERT INTO GuestStay
            (booking_id, checkin_employee_id, check_in_time_date, expected_check_out_time_date, remarks)
            VALUES (%s, %s, %s, %s, %s)
        """
       
        cursor.execute(query, (booking_id, employee_id, check_in_time, expected_checkout_time, remarks))
       
        # Update room status to Occupied
        cursor.execute("""
            UPDATE room r
            JOIN booking b ON r.room_id = b.room_id
            SET r.availability_status = 'Occupied'
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
       
        # Update guest stay with checkout time and checkout employee
        query = """
            UPDATE GuestStay
            SET actual_check_out_time_date = %s,
                checkout_employee_id = %s,
                remarks = %s
            WHERE booking_id = %s
        """
       
        cursor.execute(query, (actual_checkout_time, employee_id, remarks, booking_id))
       
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
            b.payment_status,
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
            gs.checkin_employee_id,
            gs.checkout_employee_id,
            gs.check_in_time_date,
            gs.expected_check_out_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            CONCAT(e_checkin.first_name, ' ', e_checkin.last_name) AS checkin_employee_name,
            e_checkin.emp_position AS checkin_emp_position,
            CONCAT(e_checkout.first_name, ' ', e_checkout.last_name) AS checkout_employee_name,
            e_checkout.emp_position AS checkout_emp_position
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN employee e_checkin ON gs.checkin_employee_id = e_checkin.employee_id
        LEFT JOIN employee e_checkout ON gs.checkout_employee_id = e_checkout.employee_id
        WHERE b.booking_id = %s
    """
   
    cursor.execute(query, (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()
   
    return booking




def get_pending_checkins():
    """
    Get all bookings that are ready for check-in (not yet checked in)
    Sorted by start_date (nearest first)
    Shows bookings from 7 days before start date up to 30 days in the future
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
   
    query = """
        SELECT
            b.booking_id,
            b.guest_id,
            b.room_id,
            b.booking_date,
            b.payment_status,
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
            gs.checkin_employee_id,
            gs.check_in_time_date,
            gs.expected_check_out_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            CONCAT(e.first_name, ' ', e.last_name) AS checkin_employee_name,
            DATEDIFF(b.start_date, CURDATE()) AS days_until_checkin
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN employee e ON gs.checkin_employee_id = e.employee_id
        WHERE gs.check_in_time_date IS NULL
        AND b.start_date BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE() + INTERVAL 30 DAY
        ORDER BY b.start_date ASC, b.booking_id ASC
    """
   
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
   
    return results




def get_pending_checkouts():
    """
    Get all bookings that are ready for check-out (checked in but not checked out)
    Sorted by expected_check_out_time_date (nearest first)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
   
    query = """
        SELECT
            b.booking_id,
            b.guest_id,
            b.room_id,
            b.booking_date,
            b.payment_status,
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
            gs.checkin_employee_id,
            gs.checkout_employee_id,
            gs.check_in_time_date,
            gs.expected_check_out_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            CONCAT(e_checkin.first_name, ' ', e_checkin.last_name) AS checkin_employee_name,
            CONCAT(e_checkout.first_name, ' ', e_checkout.last_name) AS checkout_employee_name,
            DATEDIFF(gs.expected_check_out_time_date, NOW()) AS days_until_checkout
        FROM booking b
        INNER JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN employee e_checkin ON gs.checkin_employee_id = e_checkin.employee_id
        LEFT JOIN employee e_checkout ON gs.checkout_employee_id = e_checkout.employee_id
        WHERE gs.check_in_time_date IS NOT NULL
        AND gs.actual_check_out_time_date IS NULL
        ORDER BY gs.expected_check_out_time_date ASC, b.booking_id ASC
    """
   
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
   
    return results
