from db import get_db_connection
from datetime import datetime

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


def create_payment(form):
    booking_id = form.get("booking_id")
    amount_paid = form.get("amount_paid")
    payment_method = form.get("payment_method")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        # --- 0. Check if payment already exists ---
        cursor.execute("SELECT payment_id FROM payment WHERE booking_id = %s", (booking_id,))
        if cursor.fetchone():
            raise Exception("Payment for this booking already exists. Cannot add again.")
        # --- 1. Fetch booking total amount ---
        cursor.execute("""
                       SELECT rt.rate_per_type, DATEDIFF(b.end_date, b.start_date) AS nights
                       FROM booking b
                                JOIN room r ON b.room_id = r.room_id
                                JOIN roomtype rt ON r.room_type_id = rt.room_type_id
                       WHERE b.booking_id = %s
                       """, (booking_id,))

        row = cursor.fetchone()
        if not row:
            raise Exception("Booking not found.")

        rate_per_night, nights = row
        total_amount = rate_per_night * nights

        # --- 2. Validate amount paid ---
        if float(amount_paid) != float(total_amount):
            raise Exception(
                f"Amount paid ({amount_paid}) does not match total ({total_amount}). Payment not accepted."
            )

        # --- 3. Insert payment ---
        cursor.execute("""
                       INSERT INTO payment (booking_id, amount_paid, payment_method, payment_datetime)
                       VALUES (%s, %s, %s, %s)
                       """, (booking_id, amount_paid, payment_method, datetime.now()))

        # --- 4. Update booking status ---
        cursor.execute("""
                       UPDATE booking
                       SET payment_status = 'Paid'
                       WHERE booking_id = %s
                       """, (booking_id,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def get_booking_total_amount(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:


        # --- 0. Check if payment already exists ---
        cursor.execute("SELECT payment_id FROM payment WHERE booking_id = %s", (booking_id,))
        if cursor.fetchone():
            raise Exception("Payment for this booking already exists. Cannot add again.")

        cursor.execute("""
            SELECT rt.rate_per_type, DATEDIFF(b.end_date, b.start_date) AS nights
            FROM booking b
            JOIN room r ON b.room_id = r.room_id
            JOIN roomtype rt ON r.room_type_id = rt.room_type_id
            WHERE b.booking_id = %s
        """, (booking_id,))
        row = cursor.fetchone()
        if not row:
            raise Exception("Booking not found")
        rate_per_night, nights = row
        return rate_per_night * nights
    finally:
        cursor.close()
        conn.close()

def get_pending_bookings_with_amount():
    """
    Fetch all bookings with payment_status = 'Pending',
    including room type, rate per night, number of nights, and total amount.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                b.booking_id,
                b.booking_date,
                rt.type_name AS room_type,
                rt.rate_per_type AS rate_per_night,
                DATEDIFF(b.end_date, b.start_date) AS number_of_nights,
                (rt.rate_per_type * DATEDIFF(b.end_date, b.start_date)) AS total_amount
            FROM booking b
            JOIN room r ON b.room_id = r.room_id
            JOIN roomtype rt ON r.room_type_id = rt.room_type_id
            WHERE b.payment_status = 'Pending'
            ORDER BY b.booking_date DESC
        """)
        bookings = cursor.fetchall()
        return bookings
    finally:
        cursor.close()
        conn.close()