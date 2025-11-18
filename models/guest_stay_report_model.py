from db import get_db_connection

def get_guest_stay_report_month(month, year):
    """
    Get guest stay report for a specific month and year
    Only includes guests who actually checked in (have GuestStay records)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            g.nationality,
            COUNT(DISTINCT gs.transaction_id) as total_stays,
            SUM(
                CASE 
                    WHEN gs.actual_check_out_time_date IS NOT NULL THEN
                        DATEDIFF(gs.actual_check_out_time_date, gs.check_in_time_date)
                    ELSE
                        DATEDIFF(CURDATE(), gs.check_in_time_date)
                END
            ) as total_nights,
            COALESCE(SUM(p.amount_paid), 0) as total_spending
        FROM GuestStay gs
        INNER JOIN booking b ON gs.booking_id = b.booking_id
        INNER JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN payment p ON b.booking_id = p.booking_id
        WHERE MONTH(gs.check_in_time_date) = %s 
          AND YEAR(gs.check_in_time_date) = %s
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address, g.nationality
        ORDER BY total_spending DESC
    """
    
    cursor.execute(query, (month, year))
    guest_stays = cursor.fetchall()
    
    # Calculate totals and nationality counts
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    # Get nationality counts
    nationality_counts = {}
    for guest in guest_stays:
        nationality = guest['nationality'] or 'Unknown'
        nationality_counts[nationality] = nationality_counts.get(nationality, 0) + 1
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum, nationality_counts

def get_guest_stay_report_year(year):
    """
    Get guest stay report for a specific year
    Only includes guests who actually checked in (have GuestStay records)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            g.nationality,
            COUNT(DISTINCT gs.transaction_id) as total_stays,
            SUM(
                CASE 
                    WHEN gs.actual_check_out_time_date IS NOT NULL THEN
                        DATEDIFF(gs.actual_check_out_time_date, gs.check_in_time_date)
                    ELSE
                        DATEDIFF(CURDATE(), gs.check_in_time_date)
                END
            ) as total_nights,
            COALESCE(SUM(p.amount_paid), 0) as total_spending
        FROM GuestStay gs
        INNER JOIN booking b ON gs.booking_id = b.booking_id
        INNER JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN payment p ON b.booking_id = p.booking_id
        WHERE YEAR(gs.check_in_time_date) = %s
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address, g.nationality
        ORDER BY total_spending DESC
    """
    
    cursor.execute(query, (year,))
    guest_stays = cursor.fetchall()
    
    # Calculate totals and nationality counts
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    # Get nationality counts
    nationality_counts = {}
    for guest in guest_stays:
        nationality = guest['nationality'] or 'Unknown'
        nationality_counts[nationality] = nationality_counts.get(nationality, 0) + 1
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum, nationality_counts