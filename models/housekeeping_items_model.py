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

def check_item_name_exists(item_name, exclude_item_id=None):
    """Check if an item name already exists (case-insensitive)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if exclude_item_id:
        # For update operations - check if name exists excluding current item
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM housekeeping_item 
            WHERE LOWER(item_name) = LOWER(%s) AND housekeeping_item_id != %s
        """, (item_name.strip(), exclude_item_id))
    else:
        # For insert operations - check if name exists anywhere
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM housekeeping_item 
            WHERE LOWER(item_name) = LOWER(%s)
        """, (item_name.strip(),))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['count'] > 0

def add_housekeeping_item_db(item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage):
    """Add a new housekeeping item to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if item name already exists
        if check_item_name_exists(item_name):
            raise Exception(f"Item name '{item_name}' already exists. Please use a different name.")
        
        cursor.execute("""
            INSERT INTO housekeeping_item (item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage)
            VALUES (%s, %s, %s, %s, %s)
        """, (item_name.strip(), cost_per_unit, current_stock, minimum_stock, max_stock_storage))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_housekeeping_item_db(item_id, item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage):
    """Update an existing housekeeping item"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if item name already exists (excluding current item)
        if check_item_name_exists(item_name, item_id):
            raise Exception(f"Item name '{item_name}' already exists. Please use a different name.")
        
        cursor.execute("""
            UPDATE housekeeping_item 
            SET item_name = %s, 
                cost_per_unit = %s, 
                current_stock = %s, 
                minimum_stock = %s, 
                max_stock_storage = %s
            WHERE housekeeping_item_id = %s
        """, (item_name.strip(), cost_per_unit, current_stock, minimum_stock, max_stock_storage, item_id))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
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

def get_all_housekeeping_employees():
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
        WHERE emp_position = 'Housekeeping'
        AND emp_status = 'Active'
        ORDER BY first_name, last_name
    """)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return employees

def get_all_admin_employees():
    """Get all employees for the issuer field - only active admin staff"""
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
        WHERE emp_position = 'Admin'
        AND emp_status = 'Active'
        ORDER BY first_name, last_name
    """)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return employees

def issue_housekeeping_items(housekeeping_item_id, quantity_issued, employee_id, issuer_id, remarks=None):
    """
    Issue housekeeping items to an employee
    - Check item availability
    - Validate employee is active housekeeping staff
    - Validate issuer is active admin staff
    - Record the issuance
    - Update item stock
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        conn.start_transaction()
        
        # 1. Validate issuer is active admin staff
        cursor.execute("""
            SELECT employee_id, emp_position, emp_status 
            FROM employee 
            WHERE employee_id = %s 
            AND emp_position = 'Admin'
            AND emp_status = 'Active'
        """, (issuer_id,))
        issuer = cursor.fetchone()
        
        if not issuer:
            raise Exception("Issuer is not authorized to issue items. Must be active admin staff.")
        
        # 2. Validate employee is active housekeeping staff
        cursor.execute("""
            SELECT employee_id, emp_position, emp_status 
            FROM employee 
            WHERE employee_id = %s 
            AND emp_position = 'Housekeeping'
            AND emp_status = 'Active'
        """, (employee_id,))
        employee = cursor.fetchone()
        
        if not employee:
            raise Exception("Employee is not authorized to receive items. Must be active housekeeping staff.")
        
        # 3. Check current stock availability
        cursor.execute("SELECT current_stock, item_name FROM housekeeping_item WHERE housekeeping_item_id = %s", 
                      (housekeeping_item_id,))
        item = cursor.fetchone()
        
        if not item:
            raise Exception("Item not found")
        
        if item['current_stock'] < quantity_issued:
            raise Exception(f"Insufficient stock. Available: {item['current_stock']}, Requested: {quantity_issued}")
        
        # 4. Record the issuance
        cursor.execute("""
            INSERT INTO housekeeping_item_issuance 
            (housekeeping_item_id, quantity_issued, employee_id, issuer_id, date_issued, remarks)
            VALUES (%s, %s, %s, %s, NOW(), %s)
        """, (housekeeping_item_id, quantity_issued, employee_id, issuer_id, remarks))
        
        # 5. Update housekeeping item stock
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

def delete_issuance_db(issuance_id):
    """Delete a specific issuance record and restore stock"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
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

def get_issuance_history():
    """Get all housekeeping item issuance history"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            hii.issuance_id,
            hi.item_name,
            hii.quantity_issued,
            CONCAT(e.first_name, ' ', e.last_name) as employee_name,
            e.emp_position as employee_position,
            CONCAT(issuer.first_name, ' ', issuer.last_name) as issuer_name,
            issuer.emp_position as issuer_position,
            hii.date_issued,
            hii.remarks
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        JOIN employee e ON hii.employee_id = e.employee_id
        JOIN employee issuer ON hii.issuer_id = issuer.employee_id
        ORDER BY hii.date_issued DESC
    """)  # Removed the LIMIT clause
    issuance_history = cursor.fetchall()
    cursor.close()
    conn.close()
    return issuance_history

def get_housekeeping_item_with_issuance_history(item_id):
    """Get housekeeping item details with issuance history to employees"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get item details
    cursor.execute("""
        SELECT 
            housekeeping_item_id,
            item_name,
            cost_per_unit,
            current_stock
        FROM housekeeping_item 
        WHERE housekeeping_item_id = %s
    """, (item_id,))
    item = cursor.fetchone()
    
    if item:
        # Get issuance history with employee details
        cursor.execute("""
            SELECT 
                hii.issuance_id,
                hii.quantity_issued,
                hii.date_issued,
                hii.remarks,
                -- Employee who received the item
                receiver.employee_id as receiver_id,
                receiver.first_name as receiver_first_name,
                receiver.last_name as receiver_last_name,
                receiver.emp_position as receiver_position,
                receiver.emp_status as receiver_status,
                -- Employee who issued the item (admin)
                issuer.employee_id as issuer_id,
                issuer.first_name as issuer_first_name,
                issuer.last_name as issuer_last_name,
                issuer.emp_position as issuer_position,
                issuer.emp_status as issuer_status
            FROM housekeeping_item_issuance hii
            JOIN employee receiver ON hii.employee_id = receiver.employee_id
            JOIN employee issuer ON hii.issuer_id = issuer.employee_id
            WHERE hii.housekeeping_item_id = %s
            ORDER BY hii.date_issued DESC
        """, (item_id,))
        issuance_history = cursor.fetchall()
        
        item['issuance_history'] = issuance_history
    
    cursor.close()
    conn.close()
    return item