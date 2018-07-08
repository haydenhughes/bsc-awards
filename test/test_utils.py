import unittest
from awards import models, db, create_app, utils


class TestUtils(unittest.TestCase):
    def test_group_size(self):
        self.assertEqual(utils.Utils.group_size(60).size, 9)
        self.assertEqual(utils.Utils.group_size(60).amount, 6)
        self.assertEqual(utils.Utils.group_size(60).last_group_size, 6)

        self.assertEqual(utils.Utils.group_size(49).size, 7)
        self.assertEqual(utils.Utils.group_size(49).amount, 7)
        self.assertEqual(utils.Utils.group_size(49).last_group_size, 0)

        self.assertEqual(utils.Utils.group_size(75).size, 7)
        self.assertEqual(utils.Utils.group_size(75).amount, 10)
        self.assertEqual(utils.Utils.group_size(75).last_group_size, 5)

        self.assertEqual(utils.Utils.group_size(51).size, 9)
        self.assertEqual(utils.Utils.group_size(51).amount, 5)
        self.assertEqual(utils.Utils.group_size(51).last_group_size, 6)


class TestStudentManager(unittest.TestCase):
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
        with utils.StudentManager() as at:
            self.assertTrue(at['HUG0005'].attending)
            self.assertFalse(at['WIL0123'].attending)

    def test_set(self):
        with utils.StudentManager() as at:
            at['ROB2134'].attending = False
            self.assertFalse(at['ROB2134'].attending)

    def test_iter(self):
        with utils.StudentManager() as at:
            students = [student_id for student_id in at]
            self.assertEqual(len(students), 2)

    def tearDown(self):
        # FIXME: Does not clear the table.
        models.Student.query.delete()
