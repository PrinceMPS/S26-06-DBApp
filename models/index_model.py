from db import get_db_connection

def get_report_cards():
    """
    Returns the list of available reports with their details
    This is a static list since these are just navigation cards
    """
    reports = [
        {
            'id': 'hotel_occupancy',
            'title': '🏨 Hotel Occupancy',
            'description': 'View room occupancy trends and current utilization.',
            'url': 'hotel_occupancy.html'
        },
        {
            'id': 'hotel_revenue',
            'title': '💰 Hotel Revenue',
            'description': 'View daily, weekly, and monthly revenue reports.',
            'url': 'http://127.0.0.1:5000/reports/hotel-revenue'
        },
        {
            'id': 'guest_stay',
            'title': '🛎️ Guest Stay',
            'description': 'Track guest stay history and check-in/check-out records.',
            'url': 'guest-stay.html'
        },
        {
            'id': 'housekeeping_usage',
            'title': '🧹 Housekeeping Usage',
            'description': 'Analyze housekeeping item consumption and stock usage.',
            'url': 'housekeeping-usage.html'
        }
    ]
    return reports