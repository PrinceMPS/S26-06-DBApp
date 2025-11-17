from db import get_db_connection
import calendar
from datetime import date


def get_total_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM room")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def get_hotel_occupancy_month(year: int, month: int):
    """
    Returns occupancy metrics for the given month/year.
    - total_rooms
    - days_in_month
    - total_room_nights
    - booked_room_nights
    - occupancy_rate (percentage)
    - daily_counts: list of {date: ISO, occupied: int}
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    days_in_month = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, days_in_month)

    total_rooms = get_total_rooms()
    total_room_nights = total_rooms * days_in_month

    # Calculate booked room-nights that overlap the month
    query = """
        SELECT SUM(DATEDIFF(LEAST(end_date, %s), GREATEST(start_date, %s)) + 1) AS booked_nights
        FROM booking
        WHERE start_date <= %s AND end_date >= %s
    """
    cursor.execute(query, (end_date, start_date, end_date, start_date))
    row = cursor.fetchone()
    booked_nights = row['booked_nights'] or 0

    occupancy_rate = 0
    if total_room_nights > 0:
        occupancy_rate = round((booked_nights / total_room_nights) * 100, 2)

    # Daily occupied rooms count
    daily_counts = []
    day_query = "SELECT COUNT(DISTINCT room_id) AS occupied FROM booking WHERE start_date <= %s AND end_date >= %s"
    for d in range(1, days_in_month + 1):
        cur_date = date(year, month, d)
        cursor.execute(day_query, (cur_date, cur_date))
        r = cursor.fetchone()
        occupied = r['occupied'] if r and r['occupied'] is not None else 0
        daily_counts.append({'date': cur_date.isoformat(), 'occupied': occupied})

    cursor.close()
    conn.close()

    return {
        'total_rooms': total_rooms,
        'days_in_month': days_in_month,
        'total_room_nights': total_room_nights,
        'booked_room_nights': booked_nights,
        'occupancy_rate': occupancy_rate,
        'daily_counts': daily_counts,
        'year': year,
        'month': month,
    }


def get_hotel_occupancy_year(year: int):
    """
    Returns occupancy metrics for the given year.
    - total_rooms
    - days_in_year
    - total_room_nights
    - booked_room_nights
    - occupancy_rate (percentage)
    - monthly_counts: list of {month: int, month_name: str, occupied_nights: int, occupancy_rate: float}
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if leap year
    days_in_year = 366 if calendar.isleap(year) else 365
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    total_rooms = get_total_rooms()
    total_room_nights = total_rooms * days_in_year

    # Calculate booked room-nights for the entire year
    query = """
        SELECT SUM(DATEDIFF(LEAST(end_date, %s), GREATEST(start_date, %s)) + 1) AS booked_nights
        FROM booking
        WHERE start_date <= %s AND end_date >= %s
    """
    cursor.execute(query, (end_date, start_date, end_date, start_date))
    row = cursor.fetchone()
    booked_nights = row['booked_nights'] or 0

    occupancy_rate = 0
    if total_room_nights > 0:
        occupancy_rate = round((booked_nights / total_room_nights) * 100, 2)

    # Monthly breakdown
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    monthly_counts = []
    for month in range(1, 13):
        days_in_month = calendar.monthrange(year, month)[1]
        month_start = date(year, month, 1)
        month_end = date(year, month, days_in_month)
        
        # Calculate booked nights for this month
        month_query = """
            SELECT SUM(DATEDIFF(LEAST(end_date, %s), GREATEST(start_date, %s)) + 1) AS booked_nights
            FROM booking
            WHERE start_date <= %s AND end_date >= %s
        """
        cursor.execute(month_query, (month_end, month_start, month_end, month_start))
        month_row = cursor.fetchone()
        month_booked_nights = month_row['booked_nights'] or 0
        
        month_total_room_nights = total_rooms * days_in_month
        month_occupancy_rate = 0
        if month_total_room_nights > 0:
            month_occupancy_rate = round((month_booked_nights / month_total_room_nights) * 100, 2)
        
        monthly_counts.append({
            'month': month,
            'month_name': month_names[month - 1],
            'occupied_nights': month_booked_nights,
            'total_room_nights': month_total_room_nights,
            'occupancy_rate': month_occupancy_rate
        })

    cursor.close()
    conn.close()

    return {
        'total_rooms': total_rooms,
        'days_in_year': days_in_year,
        'total_room_nights': total_room_nights,
        'booked_room_nights': booked_nights,
        'occupancy_rate': occupancy_rate,
        'monthly_counts': monthly_counts,
        'year': year,
    }
