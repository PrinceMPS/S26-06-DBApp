from flask import Blueprint, render_template
from models.room_details_model import get_room_with_details, get_room_guest_history

room_details_bp = Blueprint('room_details', __name__)

@room_details_bp.route('/rooms/<int:room_id>')
def room_details_page(room_id):
    # Get room details
    room = get_room_with_details(room_id)
    
    if not room:
        return "Room not found", 404
    
    # Get guest history for this room
    guest_history = get_room_guest_history(room_id)
    
    return render_template(
        'room_details.html',
        room=room,
        guest_history=guest_history
    )