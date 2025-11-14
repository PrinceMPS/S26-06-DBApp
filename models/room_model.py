from db import get_db_connection

def get_all_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.room_id,
            r.room_number,
            r.room_type,
            r.price,
            r.capacity,
            r.status,
            r.room_type_id,
            r.availability_status,
            r.housekeeping_status
        FROM room r
        ORDER BY r.room_number
    """)
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return rooms

def get_room_by_id(room_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM room WHERE room_id = %s", (room_id,))
    room = cursor.fetchone()
    cursor.close()
    conn.close()
    return room

def update_room_db(room_id, room_number, room_type, price, capacity, status, availability_status, housekeeping_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE room 
        SET room_number = %s, room_type = %s, price = %s, capacity = %s, 
            status = %s, availability_status = %s, housekeeping_status = %s
        WHERE room_id = %s
    """, (room_number, room_type, price, capacity, status, availability_status, housekeeping_status, room_id))
    conn.commit()
    cursor.close()
    conn.close()