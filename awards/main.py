import math
from flask import Blueprint, render_template, current_app
from awards import utils


bp = Blueprint('main', __name__)


@bp.route('/main/<year_level>/<page_num>')
def index(year_level, page_num):
    if year_level not in current_app.config['YEAR_LEVELS']:
        return  # TODO: Return a 404

    sm = utils.StudentManager(year_level)
    groups = utils.group_size(sm.attending)

    # TODO: Testing, unittesting
    # Account for the ammount of applauses.
    student_num = page_num - math.floor(page_num / groups.size)

    student = sm[student_num]

    awards = utils.get_awards(student.student_id)

    if (student_num % groups.size == 0) \
       or (student_num % groups.size % groups.count == 0
           and student_num % groups.last_size == 0):
        return render_template('main/applause.html')
    return render_template('main/index.html', student=student, awards=awards)
