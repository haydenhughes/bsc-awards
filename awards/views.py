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

        if (student_num % groups.size == 0) \
           or (student_num % groups.size % groups.count == 0
               and student_num % groups.last_size == 0):
            return render_template('main/applause.html')
        return render_template('main/index.html',
                               presenting='Year {}'.format(year_level),
                               year_levels=current_app.config['YEAR_LEVELS'],
                               student=student,
                               awards=awards)


class AttendanceView(FlaskView):
    def __init__(self):
        self.fullname = ''
        self.form_group = ''

    def post(self):
        with utils.StudentManager() as sm:
            student = sm.find(request.form('studentCode'))
            self.fullname = student.first_name, student.last_name
            self.form_group = student.form_group
            student.attending = request.form('attending')

    def index(self):
        return render_template('attendance/index.html',
                               presenting='BSC-Awards',
                               year_levels=current_app.config['YEAR_LEVELS'],
                               fullname=self.fullname,
                               form_group=self.form_group)
