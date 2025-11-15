from db import get_db_connection

def get_all_housekeeping_items():
    """Get all housekeeping items ordered by ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            housekeeping_item_id,
            item_name,
            cost_per_unit,
            current_stock,
            minimum_stock,
            max_stock_storage
        FROM housekeeping_item
        ORDER BY housekeeping_item_id
    """)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def get_housekeeping_item_by_id(item_id):
    """Get a specific housekeeping item by ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM housekeeping_item WHERE housekeeping_item_id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return item

def add_housekeeping_item_db(item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage):
    """Add a new housekeeping item to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO housekeeping_item (item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage)
        VALUES (%s, %s, %s, %s, %s)
    """, (item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage))
    conn.commit()
    cursor.close()
    conn.close()

def update_housekeeping_item_db(item_id, item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage):
    """Update an existing housekeeping item"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE housekeeping_item 
        SET item_name = %s, 
            cost_per_unit = %s, 
            current_stock = %s, 
            minimum_stock = %s, 
            max_stock_storage = %s
        WHERE housekeeping_item_id = %s
    """, (item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage, item_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_housekeeping_item_db(item_id):
    """Delete a housekeeping item from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM housekeeping_item WHERE housekeeping_item_id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_low_stock_items():
    """Get items where current stock is at or below minimum stock"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            housekeeping_item_id,
            item_name,
            current_stock,
            minimum_stock,
            max_stock_storage
        FROM housekeeping_item
        WHERE current_stock <= minimum_stock
        ORDER BY current_stock ASC
    """)
    low_stock_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return low_stock_items

def update_stock_level_db(item_id, new_stock_level):
    """Update the current stock level for an item"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE housekeeping_item 
        SET current_stock = %s
        WHERE housekeeping_item_id = %s
    """, (new_stock_level, item_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_housekeeping_items_usage_report(start_date, end_date):
    """Get housekeeping items usage report for a date range"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            hi.item_name,
            SUM(hii.quantity_issued) as total_quantity_issued,
            hi.cost_per_unit,
            SUM(hii.quantity_issued * hi.cost_per_unit) as total_cost
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        WHERE hii.date_issued BETWEEN %s AND %s
        AND hii.issuance_status = 'issued'
        GROUP BY hi.housekeeping_item_id, hi.item_name, hi.cost_per_unit
        ORDER BY total_quantity_issued DESC
    """, (start_date, end_date))
    report_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return report_data