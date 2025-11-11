from app import get_db_connection

def test_connection():
    conn = get_db_connection()
    if conn.is_connected():
        print("✅ Database connection successful!")
    else:
        print("❌ Failed to connect.")
    conn.close()

if __name__ == "__main__":
    test_connection()
