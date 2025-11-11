# models/booking_model.py
from db import get_db_connection

def get_all_bookings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            b.booking_id,
            b.guest_id,
            b.room_id,
            b.booking_date,
            b.start_date,
            b.end_date,
            g.first_name AS guest_first_name,
            g.last_name  AS guest_last_name
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r  ON b.room_id  = r.room_id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings
