import unittest
from awards import models, db, create_app, attendance
from config import Testing


class TestAttentanceTracker(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Testing)
        self.app.app_context().push()

        db.create_all()

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

    def test_get(self):
        self.assertTrue(self.attendance_tracker['HUG0005'])
        self.assertFalse(self.attendance_tracker['WIL0123'])

    def test_set(self):
        self.attendance_tracker['ROB2134'] = False
        self.assertFalse(self.attendance_tracker['ROB2134'])

    def test_iter(self):
        students = [student_id for student_id in self.attendance_tracker]
        self.assertEqual(len(students), 2)

    def tearDown(self):
        models.Student.query.delete()
