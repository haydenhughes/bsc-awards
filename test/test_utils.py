import unittest
import random
from awards import models, db, create_app, utils


class TestDB(unittest.TestCase):
    @classmethod
    def setUp(self):
        student_count = 60
        award_count = 5
        recipient_count = 80

        self.student_ids = []

        def generate_student():
            """Create a randomised student for testing

            Returns:
                A model.Student object.
            """
            id = ''
            for num in range(3):
                # HACK: There must be a better way
                id += random.choice(['A', 'B', 'C', 'D'])

            id += str(random.randint(0, 999))

            self.student_ids.append(id)

            attending = random.choice([True, False])

            return models.Student(student_id=id, attending=attending)

        def generate_recipient(id):
            student_id = random.choice(self.student_ids)
            award_id = random.randint(award_count)
            return models.AwardRecipients(id=id,
                                          student_id=student_id,
                                          award_id=award_id)

        app = create_app()
        app.app_context().push()

        db.create_all()

        for num in range(student_count):
            db.session.add(generate_student())

        for num in range(award_count):
            db.session.add(models.Awards(award_id=num))

        for num in range(recipient_count):
            db.session.add(generate_recipient(num))

        db.session.commit()

        self.sm = utils.StudentManager()

    def test_StudentManager_get(self):
        self.assertTrue(self.sm.get('HUG0005').attending)
        self.assertFalse(self.sm.get('WIL0123').attending)

    def test_StudentManager_get_by_index(self):
        self.assertEqual(self.sm[0].student_id, 'HUG0005')
        self.assertEqual(self.sm[2].student_id, 'ROB2134')

        with self.assertRaises(IndexError):
            self.assertEqual(self.sm[3])

    def test_StudentManager_len(self):
        self.assertEqual(len(self.sm), 3)

    def test_StudentManager_attending(self):
        self.assertEqual(self.sm.attending, 2)

    def test_get_awards(self):
        self.assertCountEqual(utils.get_awards('ROB2134'), ['Best Code Testing Award'])
        self.assertCountEqual(utils.get_awards('HUG0005'), ['Very Special Award', 'Hello World Award'])

    @classmethod
    def tearDown(self):
        models.Student.query.delete()
        models.Awards.query.delete()
        models.AwardRecipients.query.delete()
        db.session.commit()


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
