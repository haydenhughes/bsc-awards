import unittest
from awards import models, db, create_app, attendance
from config import Testing


class DBTestCase(unittest.TestCase):
    def setUpClass(self):
        self.app = create_app(Testing)
        self.attendance_tracker = attendance.AttendanceTracker()

        student_list = [('HUG0005', 'Sam', 'Wilson', True),
                        ('WIL0123', 'Jake', 'Bruckner', False),
                        ('ROB2134', 'Ben', 'Hughes', True)]

        for student_id, first_name, last_name, attending in student_list:
            student = models.Student(student_id=student_id,
                                     first_name=first_name,
                                     last_name=last_name,
                                     attending=attending)
            db.session.add(student)
        db.session.commit()
