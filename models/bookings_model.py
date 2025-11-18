from db import get_db_connection

def get_all_bookings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            b.booking_id,
            b.guest_id,
            b.room_id,
            DATE(b.booking_date) as booking_date,
            b.start_date,
            b.end_date,
            g.first_name AS guest_first_name,
            g.last_name  AS guest_last_name,
            rt.type_name as room_type
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_id = r.room_id
        LEFT JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings

def check_room_availability(room_id, start_date, end_date):
    """Check if room is available for the given dates"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT booking_id 
        FROM booking 
        WHERE room_id = %s 
        AND start_date < %s 
        AND end_date > %s
    """, (room_id, end_date, start_date))
    
    conflicting_booking = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return conflicting_booking is None

def create_booking(guest_id, room_id, start_date, end_date):
    # Check room availability first
    if not check_room_availability(room_id, start_date, end_date):
        raise Exception("Room not available for the selected dates")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Create booking with Pending payment status
        cursor.execute("""
            INSERT INTO booking (guest_id, room_id, booking_date, start_date, end_date, payment_status)
            VALUES (%s, %s, CURDATE(), %s, %s, 'Pending')
        """, (guest_id, room_id, start_date, end_date))

        # Update room status to Reserved
        cursor.execute("""
            UPDATE room SET availability_status = 'Reserved' WHERE room_id = %s
        """, (room_id,))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def search_guests(query):
    """Search guests by first name or last name"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT guest_id, first_name, last_name, contact_number, email_address
        FROM guest
        WHERE first_name LIKE %s OR last_name LIKE %s
        ORDER BY first_name, last_name
        LIMIT 10
    """, (search_term, search_term))
    
    guests = cursor.fetchall()
    cursor.close()
    conn.close()
    return guests

def get_vacant_rooms(limit=20):
    """Get list of vacant rooms with room type information"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            r.room_id,
            rt.type_name,
            rt.rate_per_type
        FROM room r
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE r.availability_status = 'Vacant'
        ORDER BY r.room_id
        LIMIT %s
    """, (limit,))
    
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return rooms