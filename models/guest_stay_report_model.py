from db import get_db_connection

def get_guest_stay_report(month, year):
    """
    Get guest stay report for a specific month and year
    Returns list of guests with their stay history and total spending
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            COUNT(DISTINCT b.booking_id) as total_stays,
            SUM(DATEDIFF(
                LEAST(b.end_date, LAST_DAY(STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))),
                GREATEST(b.start_date, STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))
            )) as total_nights,
            COALESCE(SUM(p.amount_paid), 0) as total_spending
        FROM guest g
        INNER JOIN booking b ON g.guest_id = b.guest_id
        LEFT JOIN payment p ON b.booking_id = p.booking_id
        WHERE (
            (YEAR(b.start_date) = %s AND MONTH(b.start_date) = %s) OR
            (YEAR(b.end_date) = %s AND MONTH(b.end_date) = %s) OR
            (b.start_date < STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d') AND 
             b.end_date > LAST_DAY(STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d')))
        )
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address
        HAVING total_nights > 0
        ORDER BY total_spending DESC
    """
    
    # Use the same month and year for all parameters
    params = [year, month, year, month, year, month, year, month, year, month, year, month]
    
    cursor.execute(query, params)
    guest_stays = cursor.fetchall()
    
    # Calculate totals
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum