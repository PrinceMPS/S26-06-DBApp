from db import get_db_connection

def get_all_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.room_id,
            r.room_type_id,
            r.availability_status,
            r.housekeeping_status
        FROM room r
        ORDER BY r.room_id
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