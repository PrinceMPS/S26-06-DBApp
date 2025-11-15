from db import get_db_connection


def get_all_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT 
            p.payment_id,
            p.booking_id,
            rt.type_name AS room_type,
            rt.rate_per_type AS rate_per_night,
            DATEDIFF(b.end_date, b.start_date) AS number_of_nights,
            (rt.rate_per_type * DATEDIFF(b.end_date, b.start_date)) AS total_amount,
            p.amount_paid,
            p.payment_method,
            p.payment_datetime
        FROM payment p
        JOIN booking b ON p.booking_id = b.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        ORDER BY p.payment_datetime DESC
    """)
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return payments

