from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.housekeeping_items_model import (
    get_all_housekeeping_items, 
    get_housekeeping_item_by_id, 
    add_housekeeping_item_db, 
    update_housekeeping_item_db, 
    delete_housekeeping_item_db,
    get_low_stock_items
)

# Blueprint name must match what is used in url_for()
housekeeping_bp = Blueprint('housekeeping_items', __name__)

# ---------------------------
# Display all housekeeping items
# ---------------------------
@housekeeping_bp.route('/housekeeping-items')
def housekeeping_items_page():
    items = get_all_housekeeping_items()
    return render_template('housekeeping_items.html', housekeeping_items=items)


# ---------------------------
# Edit item
# ---------------------------
@housekeeping_bp.route('/housekeeping-items/edit/<int:item_id>')
def edit_housekeeping_item(item_id):
    item = get_housekeeping_item_by_id(item_id)
    items = get_all_housekeeping_items()
    return render_template('housekeeping_items.html',
                           housekeeping_items=items,
                           editing=item)


# ---------------------------
# Add / Update / Delete
# ---------------------------
@housekeeping_bp.route('/housekeeping-items', methods=['POST'])
def handle_housekeeping_item():

    action = request.form.get('action', 'save')
    item_id = request.form.get('housekeeping_item_id')

    if action == 'delete':
        delete_housekeeping_item_db(item_id)
        flash('Item deleted successfully!', 'success')
        return redirect(url_for('housekeeping_items.housekeeping_items_page'))

    # Otherwise: add or update
    item_name = request.form.get('item_name')
    cost_per_unit = request.form.get('cost_per_unit')
    current_stock = request.form.get('current_stock')
    minimum_stock = request.form.get('minimum_stock')
    max_stock_storage = request.form.get('max_stock_storage')

    # Validate fields
    if not all([item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage]):
        flash('All fields are required.', 'error')
        return redirect(url_for('housekeeping_items.housekeeping_items_page'))

    try:
        cost_per_unit = float(cost_per_unit)
        current_stock = int(current_stock)
        minimum_stock = int(minimum_stock)
        max_stock_storage = int(max_stock_storage)
    except ValueError:
        flash('Invalid numeric values.', 'error')
        return redirect(url_for('housekeeping_items.housekeeping_items_page'))

    if item_id:  # UPDATE
        update_housekeeping_item_db(
            item_id, item_name, cost_per_unit,
            current_stock, minimum_stock, max_stock_storage
        )
        flash('Item updated successfully!', 'success')

    else:  # ADD NEW
        add_housekeeping_item_db(
            item_name, cost_per_unit, current_stock,
            minimum_stock, max_stock_storage
        )
        flash('New housekeeping item added!', 'success')

    return redirect(url_for('housekeeping_items.housekeeping_items_page'))


# ---------------------------
# LOW STOCK PAGE
# ---------------------------
@housekeeping_bp.route('/housekeeping-items/low-stock')
def low_stock_items_page():
    low_stock = get_low_stock_items()
    return render_template('low_stock_items.html', low_stock_items=low_stock)
