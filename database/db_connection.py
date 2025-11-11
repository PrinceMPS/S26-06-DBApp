import pymysql

def get_db_connection():
    """Return a new MySQL connection."""
    return pymysql.connect(
        host='localhost',
        user='your_db_user',
        password='your_db_password',
        database='Hotel_Management',
        cursorclass=pymysql.cursors.DictCursor
    )
