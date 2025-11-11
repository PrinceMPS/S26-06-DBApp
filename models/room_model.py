from app import get_db_connection  # centralized DB connection

def find_guest_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM guest WHERE email_address = %s", (email,))
    guest = cursor.fetchone()
    conn.close()
    return guest

def find_available_room(checkin_date, checkout_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Simple logic: find rooms not booked for these dates
    cursor.execute("""
        SELECT r.room_id, r.room_type
        FROM room r
        WHERE r.status = 'available'
        AND r.room_id NOT IN (
            SELECT b.room_id FROM booking b
            WHERE (b.checkin_date <= %s AND b.checkout_date >= %s)
        )
        LIMIT 1
    """, (checkout_date, checkin_date))
    room = cursor.fetchone()
    conn.close()
    return room

def update_room_status(room_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE room SET status = %s WHERE room_id = %s", (status, room_id))
    conn.commit()
    conn.close()
