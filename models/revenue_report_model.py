from db import get_db_connection

def get_hotel_revenue_report_month(year: int, month: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT rt.type_name AS room_type,
               COUNT(b.booking_id) AS total_bookings,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(b.booking_date) = %s AND MONTH(b.booking_date) = %s
        GROUP BY rt.type_name
    """
    cursor.execute(query, (year, month))
    report_data = cursor.fetchall()

    cursor.close()
    conn.close()

    grand_total = sum(row['total_revenue'] for row in report_data) if report_data else 0

    return report_data, grand_total


def get_hotel_revenue_report_year(year: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT rt.type_name AS room_type,
               COUNT(b.booking_id) AS total_bookings,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(b.booking_date) = %s
        GROUP BY rt.type_name
    """
    cursor.execute(query, (year,))
    report_data = cursor.fetchall()

    cursor.close()
    conn.close()

    grand_total = sum(row['total_revenue'] for row in report_data) if report_data else 0

    return report_data, grand_total
