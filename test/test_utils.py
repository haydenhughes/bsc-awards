import unittest
from awards import models, db, create_app, utils


class TestGroupSize(unittest.TestCase):
    def test_group_size(self):
        self.assertEqual(utils.group_size(60).size, 9)
        self.assertEqual(utils.group_size(60).count, 6)
        self.assertEqual(utils.group_size(60).last_size, 6)

        self.assertEqual(utils.group_size(49).size, 7)
        self.assertEqual(utils.group_size(49).count, 7)
        self.assertEqual(utils.group_size(49).last_size, 0)

        self.assertEqual(utils.group_size(75).size, 7)
        self.assertEqual(utils.group_size(75).count, 10)
        self.assertEqual(utils.group_size(75).last_size, 5)

        self.assertEqual(utils.group_size(51).size, 9)
        self.assertEqual(utils.group_size(51).count, 5)
        self.assertEqual(utils.group_size(51).last_size, 6)


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.app_context().push()

        db.create_all()

        self.sm = utils.StudentManager()

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
        self.assertTrue(self.sm.get('HUG0005').attending)
        self.assertFalse(self.sm.get('WIL0123').attending)

    def test_get_by_index(self):
        self.assertEqual(self.sm[0].student_id, 'HUG0005')
        self.assertEqual(self.sm[2].student_id, 'ROB2134')

        with self.assertRaises(IndexError):
            self.assertEqual(self.sm[3])

    def test_len(self):
        self.assertEqual(len(self.sm), 3)
