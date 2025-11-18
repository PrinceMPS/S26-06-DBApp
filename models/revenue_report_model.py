from db import get_db_connection

def get_hotel_revenue_report_month(year: int, month: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT rt.type_name AS room_type,
               rt.rate_per_type AS per_night_cost,
               SUM(DATEDIFF(b.end_date, b.start_date)) AS total_nights,
               COUNT(b.booking_id) AS total_bookings,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN payment p ON b.booking_id = p.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(p.payment_datetime) = %s AND MONTH(p.payment_datetime) = %s
        GROUP BY rt.type_name, rt.rate_per_type
    """

    cursor.execute(query, (year, month))
    report_data = cursor.fetchall()
    # Grand total

    grand_total = sum(row['total_revenue'] for row in report_data) if report_data else 0


    # Highest revenue room type
    cursor.execute("""
        SELECT rt.type_name AS room_type,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN payment p ON b.booking_id = p.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(p.payment_datetime) = %s AND MONTH(p.payment_datetime) = %s
        GROUP BY rt.type_name
        ORDER BY total_revenue DESC
        LIMIT 1          
                   """, (year, month))
    highest_monthly = cursor.fetchone()  # None if no bookings


    cursor.close()
    conn.close()


    return report_data, grand_total, highest_monthly

def get_hotel_revenue_report_year(year: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ----------------------------
    # 1. Monthly totals
    # ----------------------------
    cursor.execute("""
        SELECT MONTH(p.payment_datetime) AS month,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN payment p ON b.booking_id = p.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(p.payment_datetime) = %s
        GROUP BY MONTH(p.payment_datetime)
        ORDER BY MONTH(p.payment_datetime)
    """, (year,))
    monthly_rows = cursor.fetchall()

    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']


    # ----------------------------
    # 2. Room-type breakdown
    # ----------------------------
    cursor.execute("""
        SELECT rt.type_name AS room_type,
               rt.rate_per_type AS per_night_cost,
               SUM(DATEDIFF(b.end_date, b.start_date)) AS total_nights,
               COUNT(b.booking_id) AS total_bookings,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN payment p ON b.booking_id = p.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(p.payment_datetime) = %s
        GROUP BY rt.type_name, rt.rate_per_type
    """, (year,))
    report_data = cursor.fetchall()

    # ----------------------------
    # Highest revenue room type for the year
    # ----------------------------
    cursor.execute("""
        SELECT rt.type_name AS room_type,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN payment p ON b.booking_id = p.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(p.payment_datetime) = %s
        GROUP BY rt.type_name
        ORDER BY total_revenue DESC
        LIMIT 1
                   """, (year,))
    highest_yearly = cursor.fetchone()  # dict with 'room_type' and 'total_revenue'

    # ----------------------------
    # Highest revenue room type per month
    # ----------------------------
    cursor.execute("""
        SELECT MONTH(p.payment_datetime) AS month,
               rt.type_name AS room_type,
               SUM(DATEDIFF(b.end_date, b.start_date) * rt.rate_per_type) AS total_revenue
        FROM booking b
        JOIN payment p ON b.booking_id = p.booking_id
        JOIN room r ON b.room_id = r.room_id
        JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE YEAR(p.payment_datetime) = %s
        GROUP BY MONTH(p.payment_datetime), rt.type_name
        ORDER BY MONTH(p.payment_datetime), total_revenue DESC
                   """, (year,))
    month_type_rows = cursor.fetchall()

    # Process to pick the highest revenue type per month
    highest_per_month = {}
    for row in month_type_rows:
        month = row['month']
        if month not in highest_per_month:
            highest_per_month[month] = {'room_type': row['room_type'], 'total_revenue': row['total_revenue']}

    monthly_summary_with_type = []
    for row in monthly_rows:
        month_num = row['month']
        total = row['total_revenue']
        highest_type = highest_per_month.get(month_num, {}).get('room_type', '-')
        monthly_summary_with_type.append({
            'month_name': month_names[month_num - 1],
            'total_revenue': total,
            'highest_type': highest_type
        })
    cursor.close()
    conn.close()

    grand_total = sum(row['total_revenue'] for row in report_data) if report_data else 0

    return report_data, grand_total, monthly_summary_with_type, highest_yearly
