from db import get_db_connection

def get_all_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.room_id,
            r.room_type_id,
            r.availability_status,
            r.housekeeping_status,
            rt.type_name,
            rt.rate_per_type
        FROM room r
        LEFT JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        ORDER BY r.room_id
    """)
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return rooms

def get_room_by_id(room_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.*,
            rt.type_name,
            rt.rate_per_type,
            rt.capacity
        FROM room r
        LEFT JOIN roomtype rt ON r.room_type_id = rt.room_type_id
        WHERE r.room_id = %s
    """, (room_id,))
    room = cursor.fetchone()
    cursor.close()
    conn.close()
    return room

def get_next_room_number():
    """
    Generate next room number following the pattern:
    2001-2020, then 2101-2120, etc.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the highest room number
    cursor.execute("SELECT MAX(room_id) FROM room")
    max_room_id = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    if not max_room_id:
        # If no rooms exist, start with 2001
        return 2001
    
    # Calculate next room number based on pattern
    base = (max_room_id // 100) * 100  # Get the hundred base (2000, 2100, etc.)
    last_two = max_room_id % 100       # Get the last two digits
    
    if last_two < 20:
        # Still in current block (2001-2020, 2101-2120, etc.)
        return max_room_id + 1
    else:
        # Move to next block (2021 → 2101, 2121 → 2201, etc.)
        return base + 100 + 1

def add_room_db(room_id, room_type_id, availability_status, housekeeping_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO room (room_id, room_type_id, availability_status, housekeeping_status)
        VALUES (%s, %s, %s, %s)
    """, (room_id, room_type_id, availability_status, housekeeping_status))
    conn.commit()
    cursor.close()
    conn.close()

def update_room_db(room_id, availability_status, housekeeping_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE room 
        SET availability_status = %s, housekeeping_status = %s
        WHERE room_id = %s
    """, (availability_status, housekeeping_status, room_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_room_types():
    """
    Get all room types for the dropdown
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT room_type_id, type_name FROM roomtype ORDER BY room_type_id")
    room_types = cursor.fetchall()
    cursor.close()
    conn.close()
    return room_types