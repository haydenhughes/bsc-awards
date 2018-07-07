from flask import Blueprint, render_template
from awards import studenttools

bp = Blueprint('attendance', __name__)


@bp.route('/attendance')
def index():
    return render_template('attendance/index.html')
