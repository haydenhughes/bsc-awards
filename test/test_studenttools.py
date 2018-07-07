import unittest
from awards import models, db, create_app, studenttools


class TestStudent(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.app_context().push()

        db.create_all()

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
        with studenttools.StudentManager() as at:
            self.assertTrue(at['HUG0005'].attending)
            self.assertFalse(at['WIL0123'].attending)

    def test_set(self):
        with studenttools.StudentManager() as at:
            at['ROB2134'].attending = False
            self.assertFalse(at['ROB2134'].attending)

    def test_iter(self):
        with studenttools.StudentManager() as at:
            students = [student_id for student_id in at]
            self.assertEqual(len(students), 2)

    def tearDown(self):
        # FIXME: Does not clear the table.
        models.Student.query.delete()
