from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.rooms_model import get_all_rooms, get_room_by_id, update_room_db

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def rooms_page():
    rooms = get_all_rooms()
    return render_template('rooms.html', rooms=rooms)

@rooms_bp.route('/rooms/edit/<int:room_id>')
def edit_room(room_id):
    room = get_room_by_id(room_id)
    rooms = get_all_rooms()
    return render_template('rooms.html', rooms=rooms, editing=room)

@rooms_bp.route('/rooms', methods=['POST'])
def handle_room():
    room_id = request.form.get('room_id')
    availability_status = request.form.get('availability_status')
    housekeeping_status = request.form.get('housekeeping_status')
    
    try:
        update_room_db(room_id, availability_status, housekeeping_status)
        flash(f'Room #{room_id} updated successfully! Status: {availability_status}', 'success')
    except Exception as e:
        flash(f'Error updating room: {str(e)}', 'error')
    
    return redirect(url_for('rooms.rooms_page'))