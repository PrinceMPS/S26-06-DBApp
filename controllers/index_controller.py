from flask import Blueprint, render_template
from models.index_model import get_report_cards

reports_bp = Blueprint('reports', __name__, template_folder='../templates')

@reports_bp.route('/reports')
def reports_page():
    reports = get_report_cards()
    return render_template('reports/index.html', reports=reports)

