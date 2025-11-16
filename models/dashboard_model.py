from db import get_db_connection

def get_total_guests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM guest")
    total_guests = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_guests

def get_room_occupancy():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total rooms
    cursor.execute("SELECT COUNT(*) FROM room")
    total_rooms = cursor.fetchone()[0]
    
    # Occupied rooms - based on availability_status = 'Booked'
    cursor.execute("SELECT COUNT(*) FROM room WHERE availability_status = 'Occupied'")
    occupied_rooms = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    return total_rooms, occupied_rooms

def get_total_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employee WHERE emp_status = 'Active'")
    total_employees = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_employees

def get_todays_revenue():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount_paid), 0) 
        FROM payment 
        WHERE DATE(payment_datetime) = CURDATE()
    """)
    total_revenue = cursor.fetchone()[0] or 0
    cursor.close()
    conn.close()
    return float(total_revenue)


