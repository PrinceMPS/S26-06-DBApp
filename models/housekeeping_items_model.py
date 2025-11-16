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
    """Delete a housekeeping item from the database only if no issuance records exist"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if item has any issuance history
        cursor.execute("SELECT COUNT(*) as count FROM housekeeping_item_issuance WHERE housekeeping_item_id = %s", (item_id,))
        result = cursor.fetchone()
        
        if result['count'] > 0:
            raise Exception("Cannot delete item. It has issuance history. Please use the edit function to set stock to zero instead.")
        
        # If no issuance history, delete the item
        cursor.execute("DELETE FROM housekeeping_item WHERE housekeeping_item_id = %s", (item_id,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
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

def get_all_employees():
    """Get all employees for the issuance form - only active housekeeping staff"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            employee_id,
            first_name,
            last_name,
            emp_position,
            emp_status
        FROM employee
        WHERE emp_position = 'housekeeping'
        AND emp_status = 'Active'
        ORDER BY first_name, last_name
    """)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return employees

def issue_housekeeping_items(housekeeping_item_id, quantity_issued, employee_id):
    """
    Issue housekeeping items to an employee
    - Check item availability
    - Validate employee is active housekeeping staff
    - Record the issuance
    - Update item stock
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Start transaction
        conn.start_transaction()
        
        # 1. Validate employee is active housekeeping staff
        cursor.execute("""
            SELECT employee_id, emp_position, emp_status 
            FROM employee 
            WHERE employee_id = %s 
            AND emp_position = 'housekeeping'
            AND emp_status = 'Active'
        """, (employee_id,))
        employee = cursor.fetchone()
        
        if not employee:
            raise Exception("Employee is not authorized to issue items. Must be active housekeeping staff.")
        
        # 2. Check current stock availability
        cursor.execute("SELECT current_stock, item_name FROM housekeeping_item WHERE housekeeping_item_id = %s", 
                      (housekeeping_item_id,))
        item = cursor.fetchone()
        
        if not item:
            raise Exception("Item not found")
        
        if item['current_stock'] < quantity_issued:
            raise Exception(f"Insufficient stock. Available: {item['current_stock']}, Requested: {quantity_issued}")
        
        # 3. Record the issuance
        cursor.execute("""
            INSERT INTO housekeeping_item_issuance 
            (housekeeping_item_id, quantity_issued, employee_id, date_issued, issuance_status)
            VALUES (%s, %s, %s, NOW(), 'issued')
        """, (housekeeping_item_id, quantity_issued, employee_id))
        
        # 4. Update housekeeping item stock
        new_stock = item['current_stock'] - quantity_issued
        cursor.execute("""
            UPDATE housekeeping_item 
            SET current_stock = %s 
            WHERE housekeeping_item_id = %s
        """, (new_stock, housekeeping_item_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_issuance_history(limit=50):
    """Get recent housekeeping item issuance history"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            hii.issuance_id,
            hi.item_name,
            hii.quantity_issued,
            CONCAT(e.first_name, ' ', e.last_name) as employee_name,
            e.emp_position,
            hii.date_issued
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        JOIN employee e ON hii.employee_id = e.employee_id
        ORDER BY hii.date_issued DESC
        LIMIT %s
    """, (limit,))
    issuance_history = cursor.fetchall()
    cursor.close()
    conn.close()
    return issuance_history

def delete_issuance_db(issuance_id):
    """Delete a specific issuance record and restore stock"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Start transaction
        conn.start_transaction()
        
        # 1. Get the issuance details before deleting
        cursor.execute("""
            SELECT housekeeping_item_id, quantity_issued 
            FROM housekeeping_item_issuance 
            WHERE issuance_id = %s
        """, (issuance_id,))
        issuance = cursor.fetchone()
        
        if not issuance:
            raise Exception("Issuance record not found")
        
        # 2. Delete the issuance record
        cursor.execute("DELETE FROM housekeeping_item_issuance WHERE issuance_id = %s", (issuance_id,))
        
        # 3. Restore the stock to the housekeeping item
        cursor.execute("""
            UPDATE housekeeping_item 
            SET current_stock = current_stock + %s 
            WHERE housekeeping_item_id = %s
        """, (issuance['quantity_issued'], issuance['housekeeping_item_id']))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()