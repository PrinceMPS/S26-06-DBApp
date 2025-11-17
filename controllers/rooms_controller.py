from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.rooms_model import get_all_rooms, get_room_by_id, update_room_db, get_next_room_number, add_room_db, get_room_types, delete_room_db

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def rooms_page():
    rooms = get_all_rooms()
    room_types = get_room_types()
    next_room_number = get_next_room_number()
    return render_template('rooms.html', 
                         rooms=rooms, 
                         room_types=room_types,
                         next_room_number=next_room_number)

@rooms_bp.route('/rooms/edit/<int:room_id>')
def edit_room(room_id):
    room = get_room_by_id(room_id)
    rooms = get_all_rooms()
    room_types = get_room_types()
    next_room_number = get_next_room_number()
    return render_template('rooms.html', 
                         rooms=rooms, 
                         editing=room,
                         room_types=room_types,
                         next_room_number=next_room_number)

@rooms_bp.route('/rooms', methods=['POST'])
def handle_room():
    action = request.form.get('action')
    
    if action == 'add':
        # Handle adding new room
        room_id = request.form.get('room_id')
        room_type_id = request.form.get('room_type_id')
        availability_status = request.form.get('availability_status')
        
        try:
            add_room_db(room_id, room_type_id, availability_status)
            flash(f'Room #{room_id} added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding room: {str(e)}', 'error')
    
    elif action == 'update':
        # Handle updating existing room
        room_id = request.form.get('room_id')
        availability_status = request.form.get('availability_status')
        
        try:
            update_room_db(room_id, availability_status)
            flash(f'Room #{room_id} updated successfully! Status: {availability_status}', 'success')
        except Exception as e:
            flash(f'Error updating room: {str(e)}', 'error')
    
    elif action == 'delete':
        # Handle deleting room
        room_id = request.form.get('room_id')
        
        try:
            delete_room_db(room_id)
            flash(f'Room #{room_id} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting room: {str(e)}', 'error')
    
    return redirect(url_for('rooms.rooms_page'))