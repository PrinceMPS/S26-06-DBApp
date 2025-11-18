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


def get_yearly_metrics(year: int):
    """Get key metrics for yearly report"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Total Annual Spend
    total_spend_query = """
        SELECT COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_spend
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        WHERE YEAR(hii.date_issued) = %s
    """
    cursor.execute(total_spend_query, (year,))
    total_spend_result = cursor.fetchone()
    total_spend = total_spend_result['total_spend'] if total_spend_result else 0
    
    # Total Quantity Used
    total_quantity_query = """
        SELECT COALESCE(SUM(hii.quantity_issued), 0) as total_quantity
        FROM housekeeping_item_issuance hii
        WHERE YEAR(hii.date_issued) = %s
    """
    cursor.execute(total_quantity_query, (year,))
    total_quantity_result = cursor.fetchone()
    total_quantity = total_quantity_result['total_quantity'] if total_quantity_result else 0
    
    # Top 5 Most Used Items
    top_used_query = """
        SELECT 
            hi.item_name,
            SUM(hii.quantity_issued) as total_quantity
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        WHERE YEAR(hii.date_issued) = %s
        GROUP BY hi.housekeeping_item_id, hi.item_name
        ORDER BY total_quantity DESC
        LIMIT 5
    """
    cursor.execute(top_used_query, (year,))
    top_used_items = cursor.fetchall()
    
    # Highest Cost Item
    highest_cost_query = """
        SELECT 
            hi.item_name,
            SUM(hii.quantity_issued * hi.cost_per_unit) as total_cost
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        WHERE YEAR(hii.date_issued) = %s
        GROUP BY hi.housekeeping_item_id, hi.item_name
        ORDER BY total_cost DESC
        LIMIT 1
    """
    cursor.execute(highest_cost_query, (year,))
    highest_cost_item = cursor.fetchone()
    
    # Year-over-Year Change
    previous_year = year - 1
    previous_year_spend_query = """
        SELECT COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_spend
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        WHERE YEAR(hii.date_issued) = %s
    """
    cursor.execute(previous_year_spend_query, (previous_year,))
    previous_year_result = cursor.fetchone()
    previous_year_spend = previous_year_result['total_spend'] if previous_year_result else 0
    
    # Calculate YoY change
    if previous_year_spend > 0:
        yoy_change = ((total_spend - previous_year_spend) / previous_year_spend) * 100
    else:
        yoy_change = 0 if total_spend == 0 else 100
    
    cursor.close()
    conn.close()
    
    return {
        'total_spend': total_spend,
        'total_quantity': total_quantity,
        'top_used_items': top_used_items,
        'highest_cost_item': highest_cost_item,
        'yoy_change': yoy_change,
        'previous_year_spend': previous_year_spend
    }


def get_yearly_monthly_breakdown(year: int, item_id: int = None):
    """Get monthly breakdown for yearly report"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if item_id:
        # Specific item monthly breakdown
        query = """
            SELECT 
                MONTH(hii.date_issued) as month,
                SUM(hii.quantity_issued) as quantity_used,
                SUM(hii.quantity_issued * hi.cost_per_unit) as monthly_cost
            FROM housekeeping_item_issuance hii
            JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
            WHERE YEAR(hii.date_issued) = %s AND hi.housekeeping_item_id = %s
            GROUP BY MONTH(hii.date_issued)
            ORDER BY month
        """
        cursor.execute(query, (year, item_id))
    else:
        # All items monthly breakdown
        query = """
            SELECT 
                MONTH(hii.date_issued) as month,
                SUM(hii.quantity_issued) as quantity_used,
                SUM(hii.quantity_issued * hi.cost_per_unit) as monthly_cost
            FROM housekeeping_item_issuance hii
            JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
            WHERE YEAR(hii.date_issued) = %s
            GROUP BY MONTH(hii.date_issued)
            ORDER BY month
        """
        cursor.execute(query, (year,))
    
    monthly_data = cursor.fetchall()
    
    # Create a complete monthly breakdown (1-12) with zeros for missing months
    complete_monthly_data = []
    for month in range(1, 13):
        month_data = next((item for item in monthly_data if item['month'] == month), None)
        if month_data:
            complete_monthly_data.append(month_data)
        else:
            complete_monthly_data.append({
                'month': month,
                'quantity_used': 0,
                'monthly_cost': 0
            })
    
    cursor.close()
    conn.close()
    
    return complete_monthly_data


def get_specific_item_yearly_metrics(year: int, item_id: int):
    """Get yearly metrics for a specific item"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Item details and total usage
    item_query = """
        SELECT 
            hi.item_name,
            hi.cost_per_unit,
            COALESCE(SUM(hii.quantity_issued), 0) as total_quantity,
            COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as total_cost
        FROM housekeeping_item hi
        LEFT JOIN housekeeping_item_issuance hii ON hi.housekeeping_item_id = hii.housekeeping_item_id
            AND YEAR(hii.date_issued) = %s
        WHERE hi.housekeeping_item_id = %s
        GROUP BY hi.housekeeping_item_id, hi.item_name, hi.cost_per_unit
    """
    cursor.execute(item_query, (year, item_id))
    item_data = cursor.fetchone()
    
    # Previous year data for YoY calculation
    previous_year = year - 1
    previous_year_query = """
        SELECT 
            COALESCE(SUM(hii.quantity_issued * hi.cost_per_unit), 0) as previous_year_cost,
            COALESCE(SUM(hii.quantity_issued), 0) as previous_year_quantity
        FROM housekeeping_item_issuance hii
        JOIN housekeeping_item hi ON hii.housekeeping_item_id = hi.housekeeping_item_id
        WHERE YEAR(hii.date_issued) = %s AND hi.housekeeping_item_id = %s
    """
    cursor.execute(previous_year_query, (previous_year, item_id))
    previous_year_result = cursor.fetchone()
    previous_year_cost = previous_year_result['previous_year_cost'] if previous_year_result else 0
    previous_year_quantity = previous_year_result['previous_year_quantity'] if previous_year_result else 0
    
    # Calculate YoY change
    current_year_cost = item_data['total_cost'] if item_data else 0
    if previous_year_cost > 0:
        yoy_change = ((current_year_cost - previous_year_cost) / previous_year_cost) * 100
    else:
        yoy_change = 0 if current_year_cost == 0 else 100
    
    cursor.close()
    conn.close()
    
    return {
        'item_data': item_data,
        'previous_year_cost': previous_year_cost,
        'previous_year_quantity': previous_year_quantity,
        'yoy_change': yoy_change
    }


def get_available_years():
    """Get distinct years available in the database"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT DISTINCT YEAR(date_issued) as year 
        FROM housekeeping_item_issuance 
        WHERE date_issued IS NOT NULL
        ORDER BY year DESC
    """
    cursor.execute(query)
    years = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [year['year'] for year in years] if years else []


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