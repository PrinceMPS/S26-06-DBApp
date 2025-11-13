from db import get_db_connection


def get_all_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT payment_id,
                          booking_id,
                          amount_paid,
                          payment_method,
                          payment_datetime
                   FROM payment
                   ORDER BY payment_datetime DESC
                   """)
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return payments


def get_payment_by_id(payment_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payment WHERE payment_id = %s", (payment_id,))
    payment = cursor.fetchone()
    cursor.close()
    conn.close()
    return payment


def update_payment_db(payment_id, booking_id, amount_paid, payment_method):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE payment
        SET booking_id = %s, amount_paid = %s, payment_method = %s, payment_datetime =NOW()
        WHERE payment_id = %s
    """, (booking_id, amount_paid, payment_method, payment_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_payment_db(payment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payment WHERE payment_id = %s", (payment_id,))
    conn.commit()
    cursor.close()
    conn.close()
