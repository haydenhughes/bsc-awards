from flask import Blueprint, render_template, current_app

bp = Blueprint('main', __name__)


@bp.route('/main')
def index():
    return render_template('header.html')
