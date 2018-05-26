from flask import Blueprint, current_app, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html', text=current_app.config['TEXT'])