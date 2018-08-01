from flask import render_template, current_app, request, redirect, url_for, session
from flask_classful import FlaskView
from awards import utils, db, models


class LoginView(FlaskView):
    def get(self):
        return render_template('security/login.html', valid=True)

    def post(self):
        if request.form.get('username') == current_app.config['USERNAME'] \
                and request.form.get('password') == current_app.config['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('MainView:index', year_level='7', group='0', page='0'), code=302)

        else:
            return render_template('security/login.html', valid=False)


class MainView(FlaskView):
    # FIXME: Use python 3.7 type helper.
    def index(self, year_level, group, page):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'), code=302)

        if int(year_level) not in current_app.config['YEAR_LEVELS']:
            return render_template('error/404.html'), 404

        gm = utils.GroupManager(year_level=year_level)
        current_app.config['NAVBAR_BRAND'] = 'Year {}'.format(year_level)

        try:
            student_group = gm[int(group)]
        except IndexError:
            return render_template('main/completed.html')

        try:
            student = student_group[int(page)]
        except IndexError:
            return render_template('main/applause.html',
                                   year_level=int(year_level),
                                   group=int(group) + 1,
                                   page=0)
        else:
            awards = utils.get_awards(student.student_id)
            return render_template('main/index.html',
                                   student=student,
                                   awards=awards,
                                   year_level=int(year_level),
                                   group=int(group),
                                   page=int(page) + 1)


class AttendanceView(FlaskView):
    def get(self):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'))

        sm = utils.StudentManager()
        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'

        student_id = request.args.get('studentID')
        valid = True
        if student_id is None:
            student = models.Student(student_id='', first_name='', last_name='', form_group='')
        else:
            student = sm.get(student_id)
            if student is None:
                valid = False
                student = models.Student(student_id=student_id, first_name='', last_name='', form_group='')

        return render_template('attendance/index.html',
                               valid=valid,
                               student=student)

    def post(self, student_id):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'), code=302)

        sm = utils.StudentManager()
        student = sm.get(student_id)
        if student is None:
            return redirect(url_for('AttendanceView:get'), code=302)

        if request.form.get('attending') == 'checked':
            student.attending = True
        else:
            student.attending = False

        db.session.commit()

        return redirect(url_for('AttendanceView:get'), code=302)
