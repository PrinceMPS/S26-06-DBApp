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
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def add_booking(guest_id, room_id, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO booking (guest_id, room_id, booking_date, start_date, end_date)
        VALUES (%s, %s, NOW(), %s, %s)
    """, (guest_id, room_id, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()


def get_booking_by_id(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM booking WHERE booking_id = %s", (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()
    return booking


def update_booking(booking_id, guest_id, room_id, start_date, end_date):
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


def delete_booking(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM booking WHERE booking_id = %s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()
