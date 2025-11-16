from db import get_db_connection

def get_guest_stay_report(month, year):
    """
    Get guest stay report for a specific month and year
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # First, let's debug what's in the GuestStay table
    debug_query = """
        SELECT 
            gs.transaction_id,
            gs.booking_id,
            gs.check_in_time_date,
            gs.actual_check_out_time_date,
            g.guest_id,
            g.first_name,
            g.last_name
        FROM GuestStay gs
        INNER JOIN booking b ON gs.booking_id = b.booking_id
        INNER JOIN guest g ON b.guest_id = g.guest_id
        WHERE MONTH(gs.check_in_time_date) = %s 
          AND YEAR(gs.check_in_time_date) = %s
    """
    
    cursor.execute(debug_query, (month, year))
    debug_results = cursor.fetchall()
    print(f"DEBUG: Found {len(debug_results)} GuestStay records for {month}/{year}")
    for record in debug_results:
        print(f"DEBUG: GuestStay - ID: {record['transaction_id']}, Guest: {record['first_name']} {record['last_name']}, Check-in: {record['check_in_time_date']}")
    
    # Now try the main query
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
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
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address
        ORDER BY total_spending DESC
    """
    
    cursor.execute(query, (month, year))
    guest_stays = cursor.fetchall()
    
    print(f"DEBUG: Main query returned {len(guest_stays)} results")
    
    # Calculate totals
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum