from db import get_db_connection
from datetime import datetime

def get_guest_stay_report_month(month, year):
    """
    Get guest stay report for a specific month and year
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print(f"🔍 === DEBUG START: Looking for stays in {month}/{year} ===")
    
    # Debug 1: Check ALL GuestStay records to see what exists
    debug_query1 = """
        SELECT 
            gs.transaction_id,
            gs.check_in_time_date,
            gs.actual_check_out_time_date,
            g.guest_id,
            g.first_name,
            g.last_name,
            g.nationality
        FROM GuestStay gs
        JOIN booking b ON gs.booking_id = b.booking_id
        JOIN guest g ON b.guest_id = g.guest_id
        ORDER BY gs.check_in_time_date DESC
        LIMIT 20
    """
    
    cursor.execute(debug_query1)
    all_records = cursor.fetchall()
    print(f"📊 DEBUG 1: Recent GuestStay records (last 20):")
    for record in all_records:
        print(f"   Guest {record['guest_id']} - {record['first_name']} {record['last_name']} "
              f"({record['nationality']}) - Check-in: {record['check_in_time_date']} - "
              f"Check-out: {record['actual_check_out_time_date']}")

    # Debug 2: Check what exists for the specific month/year we're filtering
    debug_query2 = """
        SELECT 
            gs.transaction_id,
            gs.check_in_time_date,
            gs.actual_check_out_time_date,
            g.guest_id,
            g.first_name,
            g.last_name,
            g.nationality,
            MONTH(gs.check_in_time_date) as check_in_month,
            YEAR(gs.check_in_time_date) as check_in_year
        FROM GuestStay gs
        JOIN booking b ON gs.booking_id = b.booking_id
        JOIN guest g ON b.guest_id = g.guest_id
        WHERE MONTH(gs.check_in_time_date) = %s 
          AND YEAR(gs.check_in_time_date) = %s
    """
    
    cursor.execute(debug_query2, (month, year))
    filtered_records = cursor.fetchall()
    print(f"🎯 DEBUG 2: GuestStay records for {month}/{year}: {len(filtered_records)} records")
    
    for record in filtered_records:
        print(f"   ✅ Guest {record['guest_id']} - {record['first_name']} {record['last_name']} "
              f"({record['nationality']}) - Check-in: {record['check_in_time_date']}")

    # Debug 3: Check all nationalities in the guest table that have stays
    debug_query3 = """
        SELECT DISTINCT g.nationality, COUNT(*) as guest_count
        FROM guest g
        WHERE g.guest_id IN (
            SELECT DISTINCT b.guest_id 
            FROM booking b 
            JOIN GuestStay gs ON b.booking_id = gs.booking_id
        )
        GROUP BY g.nationality
        ORDER BY guest_count DESC
    """
    
    cursor.execute(debug_query3)
    all_nationalities = cursor.fetchall()
    print(f"🌍 DEBUG 3: All nationalities with GuestStay records:")
    for nat in all_nationalities:
        print(f"   {nat['nationality']}: {nat['guest_count']} guests")

    # Now run the actual report query (more permissive version)
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            COALESCE(g.nationality, 'Unknown') as nationality,
            COUNT(DISTINCT gs.transaction_id) as total_stays,
            COALESCE(SUM(
                CASE 
                    WHEN gs.actual_check_out_time_date IS NOT NULL AND gs.check_in_time_date IS NOT NULL THEN
                        GREATEST(DATEDIFF(gs.actual_check_out_time_date, gs.check_in_time_date), 1)
                    WHEN gs.check_in_time_date IS NOT NULL THEN
                        GREATEST(DATEDIFF(CURDATE(), gs.check_in_time_date), 1)
                    ELSE 1
                END
            ), 1) as total_nights,
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
    
    print(f"📈 DEBUG 4: Report query returned {len(guest_stays)} guests for {month}/{year}")
    for guest in guest_stays:
        print(f"   📋 Guest {guest['guest_id']} - {guest['first_name']} {guest['last_name']} "
              f"({guest['nationality']}) - {guest['total_stays']} stays, "
              f"{guest['total_nights']} nights, ₱{guest['total_spending']}")

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

    print(f"📊 DEBUG 5: Final nationality stats: {len(nationality_stats)} nationalities")
    for nat, stats in nationality_stats.items():
        print(f"   {nat}: {stats['count']} guests, {stats['total_nights']} nights, ₱{stats['total_spending']} spending")
    
    print(f"🔍 === DEBUG END ===")
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum, nationality_stats

def get_guest_stay_report_year(year):
    """
    Get guest stay report for a specific year
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print(f"🔍 === DEBUG START YEARLY: Looking for stays in {year} ===")
    
    query = """
        SELECT 
            g.guest_id,
            g.first_name,
            g.last_name,
            g.email_address,
            COALESCE(g.nationality, 'Unknown') as nationality,
            COUNT(DISTINCT gs.transaction_id) as total_stays,
            COALESCE(SUM(
                CASE 
                    WHEN gs.actual_check_out_time_date IS NOT NULL AND gs.check_in_time_date IS NOT NULL THEN
                        GREATEST(DATEDIFF(gs.actual_check_out_time_date, gs.check_in_time_date), 1)
                    WHEN gs.check_in_time_date IS NOT NULL THEN
                        GREATEST(DATEDIFF(CURDATE(), gs.check_in_time_date), 1)
                    ELSE 1
                END
            ), 1) as total_nights,
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
    
    print(f"📈 DEBUG YEARLY: Report query returned {len(guest_stays)} guests for {year}")
    
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

    print(f"📊 DEBUG YEARLY: Final nationality stats: {len(nationality_stats)} nationalities")
    print(f"🔍 === DEBUG END YEARLY ===")
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum, nationality_stats