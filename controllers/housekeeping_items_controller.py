from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.housekeeping_items_model import (
    get_all_housekeeping_items, 
    get_housekeeping_item_by_id, 
    add_housekeeping_item_db, 
    update_housekeeping_item_db, 
    delete_housekeeping_item_db,
    get_low_stock_items,
    get_all_housekeeping_employees,
    get_all_admin_employees,
    issue_housekeeping_items,
    get_issuance_history,
    delete_issuance_db,
    get_housekeeping_item_with_issuance_history,
    check_item_name_exists
)

housekeeping_bp = Blueprint('housekeeping_items', __name__)

# MAIN HOUSEKEEPING PAGE
@housekeeping_bp.route('/housekeeping-items', methods=['GET', 'POST'])
def housekeeping_items_page():
    # Handle POST requests (item management)
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            item_id = request.form.get('housekeeping_item_id')
            if item_id:
                try:
                    delete_housekeeping_item_db(item_id)
                    flash('Item deleted successfully!', 'success')
                except Exception as e:
                    flash(f'Cannot delete item: {str(e)}', 'error')
            return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory'))
        
        # Check if it's a save action (add or update)
        elif request.form.get('action') == 'save':
            # Handle save/update
            item_id = request.form.get('housekeeping_item_id')
            item_name = request.form.get('item_name', '').strip()
            cost_per_unit = request.form.get('cost_per_unit')
            current_stock = request.form.get('current_stock')
            minimum_stock = request.form.get('minimum_stock')
            max_stock_storage = request.form.get('max_stock_storage')

            # Validate fields
            if not all([item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage]):
                flash('All fields are required.', 'error')
                return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit=item_id if item_id else 'new'))

            # Validate item name is not empty after stripping
            if not item_name:
                flash('Item name cannot be empty.', 'error')
                return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit=item_id if item_id else 'new'))

            try:
                cost_per_unit = float(cost_per_unit)
                current_stock = int(current_stock)
                minimum_stock = int(minimum_stock)
                max_stock_storage = int(max_stock_storage)
                
                # Validate numeric values
                if cost_per_unit < 0 or current_stock < 0 or minimum_stock < 0 or max_stock_storage <= 0:
                    flash('All numeric values must be positive.', 'error')
                    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit=item_id if item_id else 'new'))
                    
            except ValueError:
                flash('Invalid numeric values.', 'error')
                return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit=item_id if item_id else 'new'))

            if item_id and item_id != '':  
                try:
                    update_housekeeping_item_db(
                        item_id, item_name, cost_per_unit,
                        current_stock, minimum_stock, max_stock_storage
                    )
                    flash('Item updated successfully!', 'success')
                except Exception as e:
                    flash(f'Error updating item: {str(e)}', 'error')
                    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit=item_id))
            else:  
                try:
                    add_housekeeping_item_db(
                        item_name, cost_per_unit, current_stock,
                        minimum_stock, max_stock_storage
                    )
                    flash('New housekeeping item added!', 'success')
                except Exception as e:
                    flash(f'Error adding item: {str(e)}', 'error')
                    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit='new'))
            
            return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory'))
    
    # Handle GET requests (page display)
    tab = request.args.get('tab', 'inventory')
    editing_item_id = request.args.get('edit')
    viewing_item_id = request.args.get('view_item')
    
    items = get_all_housekeeping_items()
    housekeeping_employees = get_all_housekeeping_employees()
    admin_employees = get_all_admin_employees()
    issuance_history = get_issuance_history()
    low_stock_items = get_low_stock_items()
    
    editing = None
    viewing_item = None
    
    # Handle viewing specific item
    if viewing_item_id:
        viewing_item = get_housekeeping_item_with_issuance_history(viewing_item_id)
        if not viewing_item:
            flash('Housekeeping item not found!', 'error')
            return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory'))
    
    # Handle editing
    if editing_item_id and editing_item_id != 'new':
        editing = get_housekeeping_item_by_id(editing_item_id)
    elif editing_item_id == 'new':
        editing = {
            'housekeeping_item_id': None,
            'item_name': '',
            'cost_per_unit': '',
            'current_stock': '',
            'minimum_stock': '',
            'max_stock_storage': ''
        }
    
    return render_template('housekeeping_items.html', 
                         housekeeping_items=items, 
                         employees=housekeeping_employees,
                         admin_employees=admin_employees,
                         issuance_history=issuance_history,
                         low_stock_items=low_stock_items,
                         editing=editing,
                         viewing_item=viewing_item,
                         active_tab=tab)

# EDIT ITEM ROUTE
@housekeeping_bp.route('/housekeeping-items/edit/<int:item_id>')
def edit_housekeeping_item(item_id):
    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit=item_id))

# ADD NEW ITEM ROUTE
@housekeeping_bp.route('/housekeeping-items/add')
def add_housekeeping_item():
    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='inventory', edit='new'))

# HANDLE ITEM ISSUANCE
@housekeeping_bp.route('/housekeeping-items/issue', methods=['POST'])
def handle_item_issuance():
    housekeeping_item_id = request.form.get('housekeeping_item_id')
    quantity_issued = request.form.get('quantity_issued')
    employee_id = request.form.get('employee_id')
    issuer_id = request.form.get('issuer_id')
    remarks = request.form.get('remarks', '')

    # Validate fields
    if not all([housekeeping_item_id, quantity_issued, employee_id, issuer_id]):
        flash('All fields are required for item issuance.', 'error')
        return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='issuance'))

    try:
        quantity_issued = int(quantity_issued)
        if quantity_issued <= 0:
            flash('Quantity must be greater than 0.', 'error')
            return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='issuance'))
    except ValueError:
        flash('Invalid quantity value.', 'error')
        return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='issuance'))

    try:
        issue_housekeeping_items(housekeeping_item_id, quantity_issued, employee_id, issuer_id, remarks)
        flash(f'Successfully issued {quantity_issued} items! Stock updated.', 'success')
    except Exception as e:
        flash(f'Error issuing items: {str(e)}', 'error')

    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='issuance'))

# DELETE ISSUANCE RECORD
@housekeeping_bp.route('/housekeeping-items/delete-issuance', methods=['POST'])
def delete_issuance():
    issuance_id = request.form.get('issuance_id')
    
    if issuance_id:
        try:
            delete_issuance_db(issuance_id)
            flash('Issuance record deleted successfully! Stock has been restored.', 'success')
        except Exception as e:
            flash(f'Error deleting issuance record: {str(e)}', 'error')
    
    return redirect(url_for('housekeeping_items.housekeeping_items_page', tab='issuance'))