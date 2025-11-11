from mysql.connector import connect
from app import get_db_connection  # import the centralized function
def get_db_connection():
    return connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="hotel_db"
    )



def find_guest_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM guest WHERE email_address = %s", (email,))
    guest = cursor.fetchone()
    conn.close()
    return guest

def create_guest(first_name, last_name, contact_number, email_address, nationality):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO guest (first_name, last_name, contact_number, email_address, nationality)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, last_name, contact_number, email_address, nationality))
    conn.commit()
    guest_id = cursor.lastrowid
    conn.close()
    return guest_id
