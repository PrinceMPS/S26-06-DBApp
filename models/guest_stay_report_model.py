from db import get_db_connection

def get_guest_stay_report(month, year):
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
            COUNT(DISTINCT gs.transaction_id) as total_stays,
            SUM(
                CASE 
                    WHEN gs.actual_check_out_time_date IS NOT NULL THEN
                        DATEDIFF(
                            LEAST(gs.actual_check_out_time_date, LAST_DAY(STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))),
                            GREATEST(gs.check_in_time_date, STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))
                        )
                    ELSE
                        DATEDIFF(
                            LEAST(CURDATE(), LAST_DAY(STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))),
                            GREATEST(gs.check_in_time_date, STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))
                        )
                END
            ) as total_nights,
            COALESCE(SUM(p.amount_paid), 0) as total_spending
        FROM guest g
        INNER JOIN booking b ON g.guest_id = b.guest_id
        INNER JOIN GuestStay gs ON b.booking_id = gs.booking_id
        LEFT JOIN payment p ON b.booking_id = p.booking_id
        WHERE (
            (YEAR(gs.check_in_time_date) = %s AND MONTH(gs.check_in_time_date) = %s) OR
            (gs.actual_check_out_time_date IS NOT NULL AND 
             YEAR(gs.actual_check_out_time_date) = %s AND MONTH(gs.actual_check_out_time_date) = %s) OR
            (gs.check_in_time_date < STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d') AND 
             (gs.actual_check_out_time_date IS NULL OR 
              gs.actual_check_out_time_date > LAST_DAY(STR_TO_DATE(CONCAT(%s, '-', %s, '-01'), '%%Y-%%m-%%d'))))
        )
        GROUP BY g.guest_id, g.first_name, g.last_name, g.email_address
        HAVING total_nights > 0
        ORDER BY total_spending DESC
    """
    
    # Use the same month and year for all parameters
    params = [year, month, year, month, year, month, year, month, 
              year, month, year, month, year, month, year, month]
    
    cursor.execute(query, params)
    guest_stays = cursor.fetchall()
    
    # Calculate totals
    total_nights_sum = sum(guest['total_nights'] or 0 for guest in guest_stays)
    total_spending_sum = sum(float(guest['total_spending'] or 0) for guest in guest_stays)
    
    cursor.close()
    conn.close()
    
    return guest_stays, total_nights_sum, total_spending_sum