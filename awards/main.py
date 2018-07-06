from flask import Blueprint, render_template
from flask import Blueprint, render_template, current_app

bp = Blueprint('main', __name__)


@bp.route('/main')
def index():
    return render_template('header.html')
              'Actually Comes To School Award']
    return render_template('main/index.html',
                           year_levels=current_app.config['YEAR_LEVELS'],
