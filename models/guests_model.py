from db import get_db_connection

def get_all_guests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            guest_id,
            first_name,
            last_name,
            contact_number,
            email_address,
            nationality
        FROM guest
        ORDER BY guest_id
    """)
    guests = cursor.fetchall()
    cursor.close()
    conn.close()
    return guests

def get_guest_by_id(guest_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM guest WHERE guest_id = %s", (guest_id,))
    guest = cursor.fetchone()
    cursor.close()
    conn.close()
    return guest

def add_guest_db(first_name, last_name, contact_number, email_address, nationality):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO guest (first_name, last_name, contact_number, email_address, nationality)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, last_name, contact_number, email_address, nationality))
    conn.commit()
    cursor.close()
    conn.close()

def update_guest_db(guest_id, first_name, last_name, contact_number, email_address, nationality):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE guest 
        SET first_name = %s, last_name = %s, contact_number = %s, 
            email_address = %s, nationality = %s
        WHERE guest_id = %s
    """, (first_name, last_name, contact_number, email_address, nationality, guest_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_guest_db(guest_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guest WHERE guest_id = %s", (guest_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_guest_full_details(guest_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Guest basic info
    cursor.execute("SELECT * FROM guest WHERE guest_id = %s", (guest_id,))
    guest = cursor.fetchone()

    # 2. Guest bookings
    cursor.execute("""
        SELECT 
            b.booking_id,
            b.room_id,
            r.room_type_id,
            rt.type_name,
            b.start_date,
            b.end_date,
            COALESCE(p.amount_paid, 0) as total_cost,
            p.payment_method
        FROM booking b
        JOIN room r ON b.room_id = r.room_id
        JOIN RoomType rt ON r.room_type_id = rt.room_type_id
        LEFT JOIN payment p ON b.booking_id = p.booking_id
        WHERE b.guest_id = %s
        ORDER BY b.start_date DESC
    """, (guest_id,))
    bookings = cursor.fetchall()

    # 3. Guest stays
    cursor.execute("""
        SELECT 
            gs.transaction_id,
            gs.booking_id,
            gs.check_in_time_date,
            gs.actual_check_out_time_date,
            gs.employee_id,
            e.first_name AS employee_first_name,
            e.last_name AS employee_last_name
        FROM GuestStay gs
        LEFT JOIN employee e ON gs.employee_id = e.employee_id
        JOIN booking b ON gs.booking_id = b.booking_id
        WHERE b.guest_id = %s
        ORDER BY gs.check_in_time_date DESC
    """, (guest_id,))
    guest_stays = cursor.fetchall()

    cursor.close()
    conn.close()

    return guest, bookings, guest_stays
