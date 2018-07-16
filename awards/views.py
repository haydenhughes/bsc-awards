import math
from flask import render_template, current_app, request
from flask_classful import FlaskView
from awards import utils


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
    def __init__(self):
        self.fullname = ''
        self.form_group = ''
        self.attending = False

    def get(self):
        # TEMP: Somehow I don't think request.get will work
        student = request.get('studentCode')
        self.fullname = student.first_name, student.last_name
        self.form_group = student.form_group
        self.attending = student.attending
        current_app.config['NAVBAR_BRAND'] = 'BSC Awards'
        return render_template('attendance/index.html',
                               fullname=self.fullname,
                               form_group=self.form_group,
                               attending=self.attending)

    def post(self):
        with utils.StudentManager() as sm:
            # TODO: Invalid student code handling
            # FIXME: request.form is not working
            student = sm.get(request.form('studentCode'))
            student.attending = request.form('attending')
