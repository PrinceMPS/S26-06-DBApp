from db import get_db_connection

def get_items_usage_report_month(year: int, month: int, item_id: int = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if item_id:
        # Specific item report
        query = """
            SELECT 
                hi.item_name,
                hi.cost_per_unit,
                COALESCE(SUM(hii.quantity_issued), 0) as quantity_used,
                COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_cost
            FROM housekeeping_item hi
            LEFT JOIN housekeeping_item_issuance hii ON hi.housekeeping_item_id = hii.housekeeping_item_id
                AND YEAR(hii.date_issued) = %s 
                AND MONTH(hii.date_issued) = %s
            WHERE hi.housekeeping_item_id = %s
            GROUP BY hi.housekeeping_item_id, hi.item_name, hi.cost_per_unit
        """
        cursor.execute(query, (year, month, item_id))
    else:
        # All items report
        query = """
            SELECT 
                hi.item_name,
                hi.cost_per_unit,
                COALESCE(SUM(hii.quantity_issued), 0) as quantity_used,
                COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_cost
            FROM housekeeping_item hi
            LEFT JOIN housekeeping_item_issuance hii ON hi.housekeeping_item_id = hii.housekeeping_item_id
                AND YEAR(hii.date_issued) = %s 
                AND MONTH(hii.date_issued) = %s
            GROUP BY hi.housekeeping_item_id, hi.item_name, hi.cost_per_unit
            HAVING quantity_used > 0
            ORDER BY quantity_used DESC
        """
        cursor.execute(query, (year, month))
    
    report_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Calculate totals
    grand_total = sum(row['total_cost'] for row in report_data) if report_data else 0
    total_quantity = sum(row['quantity_used'] for row in report_data) if report_data else 0

    return report_data, grand_total, total_quantity


def get_items_usage_report_year(year: int, item_id: int = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if item_id:
        # Specific item report
        query = """
            SELECT 
                hi.item_name,
                hi.cost_per_unit,
                COALESCE(SUM(hii.quantity_issued), 0) as quantity_used,
                COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_cost
            FROM housekeeping_item hi
            LEFT JOIN housekeeping_item_issuance hii ON hi.housekeeping_item_id = hii.housekeeping_item_id
                AND YEAR(hii.date_issued) = %s
            WHERE hi.housekeeping_item_id = %s
            GROUP BY hi.housekeeping_item_id, hi.item_name, hi.cost_per_unit
        """
        cursor.execute(query, (year, item_id))
    else:
        # All items report
        query = """
            SELECT 
                hi.item_name,
                hi.cost_per_unit,
                COALESCE(SUM(hii.quantity_issued), 0) as quantity_used,
                COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_cost
            FROM housekeeping_item hi
            LEFT JOIN housekeeping_item_issuance hii ON hi.housekeeping_item_id = hii.housekeeping_item_id
                AND YEAR(hii.date_issued) = %s
            GROUP BY hi.housekeeping_item_id, hi.item_name, hi.cost_per_unit
            HAVING quantity_used > 0
            ORDER BY quantity_used DESC
        """
        cursor.execute(query, (year,))
    
    report_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Calculate totals
    grand_total = sum(row['total_cost'] for row in report_data) if report_data else 0
    total_quantity = sum(row['quantity_used'] for row in report_data) if report_data else 0

    return report_data, grand_total, total_quantity


def get_all_housekeeping_items():
    """Get all housekeeping items for the dropdown"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT housekeeping_item_id, item_name 
        FROM housekeeping_item 
        ORDER BY item_name
    """)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items