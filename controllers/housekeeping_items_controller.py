from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.housekeeping_items_model import (
    get_all_housekeeping_items, 
    get_housekeeping_item_by_id, 
    add_housekeeping_item_db, 
    update_housekeeping_item_db, 
    delete_housekeeping_item_db,
    get_low_stock_items
)

housekeeping_bp = Blueprint('housekeeping', __name__)

@housekeeping_bp.route('/housekeeping-items')
def housekeeping_items_page():
    """Display all housekeeping items"""
    items = get_all_housekeeping_items()
    return render_template('admin/housekeeping-items.html', housekeeping_items=items)

@housekeeping_bp.route('/housekeeping-items/edit/<int:item_id>')
def edit_housekeeping_item(item_id):
    """Edit a specific housekeeping item"""
    item = get_housekeeping_item_by_id(item_id)
    items = get_all_housekeeping_items()
    return render_template('admin/housekeeping-items.html', housekeeping_items=items, editing=item)

@housekeeping_bp.route('/housekeeping-items', methods=['POST'])
def handle_housekeeping_item():
    """Handle add, update, and delete operations for housekeeping items"""
    action = request.form.get('action', 'save')
    item_id = request.form.get('housekeeping_item_id')
    
    if action == 'delete':
        # Handle delete
        try:
            delete_housekeeping_item_db(item_id)
            flash('Housekeeping item deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting housekeeping item: {str(e)}', 'error')
    else:
        # Handle add/update
        item_name = request.form.get('item_name')
        cost_per_unit = request.form.get('cost_per_unit')
        current_stock = request.form.get('current_stock')
        minimum_stock = request.form.get('minimum_stock')
        max_stock_storage = request.form.get('max_stock_storage')
        
        # Basic validation
        if not all([item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage]):
            flash('All fields are required', 'error')
            return redirect(url_for('housekeeping.housekeeping_items_page'))
        
        # Convert numeric fields
        try:
            cost_per_unit = float(cost_per_unit)
            current_stock = int(current_stock)
            minimum_stock = int(minimum_stock)
            max_stock_storage = int(max_stock_storage)
            
            # Additional validation
            if cost_per_unit < 0:
                flash('Cost per unit cannot be negative', 'error')
                return redirect(url_for('housekeeping.housekeeping_items_page'))
            
            if current_stock < 0:
                flash('Current stock cannot be negative', 'error')
                return redirect(url_for('housekeeping.housekeeping_items_page'))
            
            if minimum_stock < 0:
                flash('Minimum stock cannot be negative', 'error')
                return redirect(url_for('housekeeping.housekeeping_items_page'))
            
            if max_stock_storage <= 0:
                flash('Max storage must be greater than 0', 'error')
                return redirect(url_for('housekeeping.housekeeping_items_page'))
            
            if current_stock > max_stock_storage:
                flash('Current stock cannot exceed maximum storage capacity', 'error')
                return redirect(url_for('housekeeping.housekeeping_items_page'))
                
        except ValueError:
            flash('Please enter valid numeric values', 'error')
            return redirect(url_for('housekeeping.housekeeping_items_page'))
        
        try:
            if item_id:  # Update existing item
                update_housekeeping_item_db(item_id, item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage)
                flash('Housekeeping item updated successfully!', 'success')
            else:  # Add new item
                add_housekeeping_item_db(item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage)
                flash('Housekeeping item added successfully!', 'success')
        except Exception as e:
            flash(f'Error saving housekeeping item: {str(e)}', 'error')
    
    return redirect(url_for('housekeeping.housekeeping_items_page'))

@housekeeping_bp.route('/housekeeping-items/low-stock')
def low_stock_items():
    """Display low stock items"""
    low_stock_items = get_low_stock_items()
    return render_template('admin/low_stock_items.html', low_stock_items=low_stock_items)