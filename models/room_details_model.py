from db import get_db_connection

def get_room_with_details(room_id):
    """
    Get room details with room type information
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.*,
            rt.type_name,
            rt.rate_per_type,
            rt.capacity
        FROM room r
        LEFT JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE r.room_id = %s
    """, (room_id,))
    room = cursor.fetchone()
    cursor.close()
    conn.close()
    return room

def get_room_guest_history(room_id):
    """
    Get all guests who stayed in this room with their stay details
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            g.contact_number,
            b.booking_id,
            b.start_date,
            b.end_date,
            gs.check_in_time_date,
            gs.actual_check_out_time_date,
            gs.remarks,
            p.amount_paid,
            p.payment_method
        FROM booking b
        INNER JOIN guest g ON b.guest_id = g.guest_id
        INNER JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN payment p ON b.booking_id = p.booking_id
        WHERE b.room_id = %s
        ORDER BY gs.check_in_time_date DESC
    """, (room_id,))
    guest_history = cursor.fetchall()
    cursor.close()
    conn.close()
    return guest_history