from flask import Blueprint, render_template, request
from awards import studenttools

bp = Blueprint('attendance', __name__)


@bp.route('/attendance', methods=['GET', 'POST'])
def index():
    fullname = ''
    form_group = ''

    if request.method == 'POST':
        with studenttools.StudentTracker as at:
            student = at[request.form('studentCode')]
            fullname = student.first_name, student.last_name
            form_group = student.form_group
            student.attending = request.form('attending')

    return render_template('attendance/index.html',
                           fullname=fullname,
                           form_group=form_group)
