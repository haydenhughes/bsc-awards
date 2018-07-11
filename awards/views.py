import math
from flask import render_template, current_app, request
from flask.ext.classful import FlaskView
from awards import utils


class MainView(FlaskView):
    def index(self, year_level, page):
        if year_level not in current_app.config['YEAR_LEVELS']:
            return  # TODO: Return a 404

        sm = utils.StudentManager(year_level)
        groups = utils.group_size(sm.attending)

        # TODO: Testing, unittesting
        # Account for the ammount of applauses.
        student_num = page - math.floor(page / groups.size)

        student = sm[student_num]

        awards = utils.get_awards(student.student_id)

        if (student_num % groups.size == 0) \
           or (student_num % groups.size % groups.count == 0
               and student_num % groups.last_size == 0):
            return render_template('main/applause.html')
        return render_template('main/index.html', student=student, awards=awards)


class AttendanceView(FlaskView):
    def post(self):
        with utils.StudentManager() as sm:
            student = sm.find(request.form('studentCode'))
            self.fullname = student.first_name, student.last_name
            self.form_group = student.form_group
            student.attending = request.form('attending')

    def index(self):
        return render_template('attendance/index.html',
                               fullname=self.fullname,
                               form_group=self.form_group)
