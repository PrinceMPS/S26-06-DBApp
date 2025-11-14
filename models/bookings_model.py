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
            g.last_name  AS guest_last_name
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings

def get_booking_by_id(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM booking WHERE booking_id = %s", (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()
    return booking

def check_room_availability(room_id, start_date, end_date, exclude_booking_id=None):
    """
    Check if room is available for the given dates
    Returns True if available, False if conflicted
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT booking_id 
        FROM booking 
        WHERE room_id = %s 
        AND start_date < %s 
        AND end_date > %s
        AND booking_id != %s
    """
    
    params = [room_id, end_date, start_date, exclude_booking_id or 0]
    
    cursor.execute(query, params)
    conflicting_booking = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return conflicting_booking is None

def get_conflicting_booking(room_id, start_date, end_date, exclude_booking_id=None):
    """
    Get details of conflicting booking if exists
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT b.booking_id, b.guest_id, b.start_date, b.end_date,
               g.first_name, g.last_name
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        WHERE b.room_id = %s 
        AND b.start_date < %s 
        AND b.end_date > %s
        AND b.booking_id != %s
        ORDER BY b.booking_date ASC
        LIMIT 1
    """
    
    params = [room_id, end_date, start_date, exclude_booking_id or 0]
    
    cursor.execute(query, params)
    conflict = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return conflict


def create_booking_with_payment(guest_id, room_id, start_date, end_date, amount_paid, payment_method):
    # Check room availability first
    if not check_room_availability(room_id, start_date, end_date):
        conflict = get_conflicting_booking(room_id, start_date, end_date)
        raise Exception(
            f"Room not available. Conflicting with booking #{conflict['booking_id']} for {conflict['first_name']} {conflict['last_name']} from {conflict['start_date']} to {conflict['end_date']}")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Start transaction
        cursor.execute("""
                       INSERT INTO booking (guest_id, room_id, booking_date, start_date, end_date)
                       VALUES (%s, %s, CURDATE(), %s, %s)
                       """, (guest_id, room_id, start_date, end_date))

        booking_id = cursor.lastrowid  # get the inserted booking's ID

        # Insert payment linked to the booking
        cursor.execute("""
                       INSERT INTO payment (booking_id, amount_paid, payment_method, payment_datetime)
                       VALUES (%s, %s, %s, NOW())
                       """, (booking_id, amount_paid, payment_method))

        conn.commit()  # commit both inserts together
        return booking_id

    except Exception as e:
        conn.rollback()  # undo both inserts if anything fails
        raise e
    finally:
        cursor.close()
        conn.close()


def update_booking_db(booking_id, guest_id, room_id, start_date, end_date):
    # Check availability excluding current booking
    if not check_room_availability(room_id, start_date, end_date, booking_id):
        conflict = get_conflicting_booking(room_id, start_date, end_date, booking_id)
        raise Exception(f"Room not available. Conflicting with booking #{conflict['booking_id']} for {conflict['first_name']} {conflict['last_name']} from {conflict['start_date']} to {conflict['end_date']}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE booking
        SET guest_id = %s, room_id = %s, start_date = %s, end_date = %s
        WHERE booking_id = %s
    """, (guest_id, room_id, start_date, end_date, booking_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_booking_db(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM booking WHERE booking_id = %s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()


#to get amount in exeisting bookings
def get_booking_total_amount(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) #access column names as keys

    query = """
            SELECT b.booking_id, \
                   r.room_id, \
                   rt.type_name, \
                   rt.rate_per_type, \
                   DATEDIFF(b.end_date, b.start_date)                      AS nights, \
                   (rt.rate_per_type * DATEDIFF(b.end_date, b.start_date)) AS total_amount
            FROM booking b
                     JOIN room r ON b.room_id = r.room_id
                     JOIN roomtype rt ON r.room_type_id = rt.room_type_id
            WHERE b.booking_id = %s; \
            """

    cursor.execute(query, (booking_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def get_booking_total_amount_for_new(room_id, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT rt.rate_per_type,
               DATEDIFF(%s, %s) AS nights,
               (rt.rate_per_type * DATEDIFF(%s, %s)) AS total_amount
        FROM room r
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE r.room_id = %s
    """
    cursor.execute(query, (end_date, start_date, end_date, start_date, room_id))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        raise Exception("Room not found")
    if result['nights'] <= 0:
        raise Exception("End date must be after start date")

    return result['total_amount']

