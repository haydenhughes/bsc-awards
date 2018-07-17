import math
from flask import render_template, current_app, request, redirect, url_for
from flask_classful import FlaskView
from awards import utils, db


class MainView(FlaskView):
    # FIXME: Use python 3.7 type helper.
    def index(self, year_level, page):
        if int(year_level) not in current_app.config['YEAR_LEVELS']:
            return 404

        sm = utils.StudentManager(year_level)
        groups = utils.group_size(sm.attending)

        # Account for the ammount of applauses.
        student_num = int(page) - math.floor(int(page) / groups.size)

        student = sm[student_num]

        awards = utils.get_awards(student.student_id)

        current_app.config['NAVBAR_BRAND'] = 'Year {}'.format(year_level)

        if (student_num % groups.size == 0) \
           or (student_num % groups.size % groups.count == 0
               and student_num % groups.last_size == 0):
            return render_template('main/applause.html',
                                   year_level=int(year_level), page=int(page))
        return render_template('main/index.html',
                               student=student,
                               awards=awards,
                               year_level=int(year_level),
                               page=int(page))


class AttendanceView(FlaskView):
    def get(self):
        sm = utils.StudentManager()
        student = sm.get(request.args.get('studentCode'))
        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'
        return render_template('attendance/index.html',
                               student=student)

    def post(self, student_id):
        sm = utils.StudentManager()
        student = sm.get(student_id)
        if request.form.get('attending') == 'checked':
            student.attending = True
        else:
            student.attending = False

        db.session.commit()

        return redirect(url_for('AttendanceView:get'), code=302)
