import pymysql

def get_db_connection():
    """Return a new MySQL connection."""
    return pymysql.connect(
        host='localhost',
        user='root',
        password='maT168mit',
        database='Hotel_Management',
        cursorclass=pymysql.cursors.DictCursor
    )