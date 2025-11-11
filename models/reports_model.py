from database.db_connection import get_db_connection

def get_total_booked_days_by_room(room_id, month, year):
    """
    Calculate total booked days for a specific room in a given month/year.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Compute first and last day of month
    start_of_month = f"{year}-{month:02d}-01"
    if month == 12:
        end_of_month = f"{year}-12-31"
    else:
        end_of_month = f"{year}-{month+1:02d}-01"

    # TODO: Add SQL query here to calculate total booked days
    query = """
        SELECT SUM(DATEDIFF(
            LEAST(end_date, %s),
            GREATEST(start_date, %s)
        ) + 1) AS total_days_booked
        FROM booking
        WHERE room_id = %s
          AND start_date < %s
          AND end_date >= %s
    """
    
    cursor.execute(query, (end_of_month, start_of_month, room_id, end_of_month, start_of_month))
    result = cursor.fetchone()['total_days_booked'] or 0

    cursor.close()
    conn.close()

    return result
