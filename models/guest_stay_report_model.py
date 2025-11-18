from db import get_db_connection

def get_guest_stay_report_month(month, year):
    """
    Get guest stay report for a specific month and year
    Less restrictive filters to catch more transactions
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # First, let's debug what's actually in the database
    debug_query = """
        SELECT 
            gs.transaction_id,
            gs.check_in_time_date,
            gs.actual_check_out_time_date,
            g.guest_id,
            g.first_name,
            g.last_name,
            g.nationality,
            DATEDIFF(
                COALESCE(gs.actual_check_out_time_date, CURDATE()), 
                gs.check_in_time_date
            ) as calculated_nights
        FROM GuestStay gs
        JOIN booking b ON gs.booking_id = b.booking_id
        JOIN guest g ON b.guest_id = g.guest_id
        WHERE MONTH(gs.check_in_time_date) = %s 
          AND YEAR(gs.check_in_time_date) = %s
    """
    
    cursor.execute(debug_query, (month, year))
    debug_results = cursor.fetchall()
    print(f"DEBUG: Found {len(debug_results)} GuestStay records for {month}/{year}")
    for record in debug_results:
        print(f"DEBUG: Guest {record['guest_id']} - Check-in: {record['check_in_time_date']} - Check-out: {record['actual_check_out_time_date']} - Nights: {record['calculated_nights']}")
    
    # Now run the actual report query with less restrictive filters
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            COALESCE(g.nationality, 'Unknown') as nationality,
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
          AND gs.check_in_time_date IS NOT NULL  # Only require check-in
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address, g.nationality
        ORDER BY total_spending DESC
    """
    
    cursor.execute(query, (month, year))
    guest_stays = cursor.fetchall()
    
    print(f"DEBUG: Report query returned {len(guest_stays)} guests")
    
    # Calculate totals
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    # Get nationality statistics
    nationality_stats = {}
    for guest in guest_stays:
        nationality = guest['nationality']
        if nationality not in nationality_stats:
            nationality_stats[nationality] = {
                'count': 0,
                'total_nights': 0,
                'total_spending': 0
            }
        
        nationality_stats[nationality]['count'] += 1
        nationality_stats[nationality]['total_nights'] += guest['total_nights'] or 0
        nationality_stats[nationality]['total_spending'] += float(guest['total_spending'] or 0)
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum, nationality_stats

def get_guest_stay_report_year(year):
    """
    Get guest stay report for a specific year
    Less restrictive filters
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            COALESCE(g.nationality, 'Unknown') as nationality,
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
          AND gs.check_in_time_date IS NOT NULL  # Only require check-in
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address, g.nationality
        ORDER BY total_spending DESC
    """
    
    cursor.execute(query, (year,))
    guest_stays = cursor.fetchall()
    
    # Calculate totals
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    # Get nationality statistics
    nationality_stats = {}
    for guest in guest_stays:
        nationality = guest['nationality']
        if nationality not in nationality_stats:
            nationality_stats[nationality] = {
                'count': 0,
                'total_nights': 0,
                'total_spending': 0
            }
        
        nationality_stats[nationality]['count'] += 1
        nationality_stats[nationality]['total_nights'] += guest['total_nights'] or 0
        nationality_stats[nationality]['total_spending'] += float(guest['total_spending'] or 0)
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum, nationality_stats