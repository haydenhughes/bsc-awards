from flask import render_template, current_app, request, redirect, url_for
from flask_classful import FlaskView
from awards import utils, db


class MainView(FlaskView):
    # FIXME: Use python 3.7 type helper.
    def index(self, year_level, group, page):
        if int(year_level) not in current_app.config['YEAR_LEVELS']:
            return 404

        gm = utils.GroupManager(year_level=year_level)
        current_app.config['NAVBAR_BRAND'] = 'Year {}'.format(year_level)

        try:
            group = gm[group]
        except IndexError:
            # TEMP: No more groups code here
            pass

        try:
            student = group[page]
        except IndexError:
            return render_template('main/applause.html',
                                   year_level=int(year_level),
                                   page=int(page),
                                   page_count=page_count)
        else:
            awards = utils.get_awards(student.student_id)
            return render_template('main/index.html',
                                   student=student,
                                   awards=awards,
                                   year_level=int(year_level),
                                   page=int(page),
                                   page_count=page_count)


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
