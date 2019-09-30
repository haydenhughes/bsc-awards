from flask import render_template, current_app, request, redirect, url_for, session
from flask_classful import FlaskView
from flask_table import Table, Col, NestedTableCol
from awards import utils


class IndexView(FlaskView):
    route_base = '/'

    def index(self):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'), code=302)

        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'

        return render_template('index.html')


class LoginView(FlaskView):
    def get(self):
        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'

        logout = False
        if request.args.get('logout') == '1' and session.get('logged_in'):
            session['logged_in'] = False
            logout = True

        return render_template('security/login.html', valid=True, logout=logout)

    def post(self):
        if request.form.get('username') == current_app.config['USERNAME'] \
                and request.form.get('password') == current_app.config['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('IndexView:index'), code=302)

        else:
            return render_template('security/login.html', valid=False, logout=False)


class LogoutView(FlaskView):
    def index(self):
        return redirect(url_for('LoginView:get') + '?logout=1')


class MainView(FlaskView):
    def index(self, year_level: int):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'), code=302)

        if year_level not in current_app.config['YEAR_LEVELS']:
            return render_template('error/404.html'), 404

        gm = utils.GroupManager(year_levels=[year_level])
        current_app.config['NAVBAR_BRAND'] = 'Year {}'.format(year_level)

        return render_template('main/index.html')


class AttendanceView(FlaskView):
    def get(self):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'))

        sm = utils.StudentManager()
        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'

        student_id = request.args.get('studentID')
        student = sm.get(student_id)

        return render_template('attendance/index.html', student=student)

    def post(self, student_id):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'), code=302)

        with utils.StudentManager() as sm:
            student = sm.get(student_id)
            if student is None:
                return redirect(url_for('AttendanceView:get'), code=302)

            if request.form.get('attending') == 'checked':
                student.attending = True
            else:
                student.attending = False

        return redirect(url_for('AttendanceView:get'), code=302)


class AwardsSubTable(Table):
    classes = ['table', 'table-sm', 'd-print-table-row']
    award = Col('Awards')
    thead_classes = ['d-none']


class AttendanceTable(Table):
    classes = ['table', 'table-bordered', 'd-print-table-row']
    name = Col('Full Name')
    awards = NestedTableCol('Awards', AwardsSubTable)


class PrintView(FlaskView):
    def index(self, year_level: int):
        if not session.get('logged_in'):
            return redirect(url_for('LoginView:get'))

        if year_level == 0:
            sm = utils.StudentManager()
        else:
            sm = utils.StudentManager(year_levels=[year_level])

        rows = []

        for student in sm:
            if student.preferred_name is not None:
                name = '{} {}'.format(student.preferred_name, student.last_name)
            else:
                name = '{} {}'.format(student.first_name, student.last_name)

            awards_table = AwardsSubTable(student.awards())
            rows.append(dict(name=name, awards=awards_table))

        table = AttendanceTable(rows)

        return render_template('attendance/print.html', year_level=year_level, table=table)
