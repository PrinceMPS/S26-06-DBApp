from db import get_db_connection

def get_all_guests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            guest_id,
            first_name,
            last_name,
            contact_number,
            email_address,
            nationality
        FROM guest
        ORDER BY guest_id
    """)
    guests = cursor.fetchall()
    cursor.close()
    conn.close()
    return guests

def get_guest_by_id(guest_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM guest WHERE guest_id = %s", (guest_id,))
    guest = cursor.fetchone()
    cursor.close()
    conn.close()
    return guest

def add_guest_db(first_name, last_name, contact_number, email_address, nationality):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO guest (first_name, last_name, contact_number, email_address, nationality)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, last_name, contact_number, email_address, nationality))
    conn.commit()
    cursor.close()
    conn.close()

def update_guest_db(guest_id, first_name, last_name, contact_number, email_address, nationality):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE guest 
        SET first_name = %s, last_name = %s, contact_number = %s, 
            email_address = %s, nationality = %s
        WHERE guest_id = %s
    """, (first_name, last_name, contact_number, email_address, nationality, guest_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_guest_db(guest_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guest WHERE guest_id = %s", (guest_id,))
    conn.commit()
    cursor.close()
    conn.close()