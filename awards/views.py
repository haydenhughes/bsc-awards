import math
from flask import render_template, current_app, request, redirect, url_for
from flask_classful import FlaskView
from awards import utils, models, db


class MainView(FlaskView):
    # FIXME: Use python 3.7 type helper.
    def index(self, year_level, page):
        if int(year_level) not in current_app.config['YEAR_LEVELS']:
            # TODO: Better 404 page
            return '404 Year not valid.'

        sm = utils.StudentManager(year_level)
        groups = utils.group_size(sm.attending)

        # TODO: Testing, unittesting
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
        self.student = sm.get(request.args.get('studentCode'))
        print('GET RAN')
        print(self.student)

        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'
        return render_template('attendance/index.html',
                               student=self.student)

    def post(self):
        if request.form.get('attending') == 'checked':
            self.student.attending = True
        else:
            self.student.attending = False

        db.session.commit()

        print("RAN POST")
        print(models.Student.query.filter_by(student_id=self.student.student_id).first().attending)

        return redirect(url_for('AttendanceView:get'), code=302)
