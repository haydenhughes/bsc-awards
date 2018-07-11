import unittest
from awards import models, db, create_app, utils


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.app_context().push()

        db.create_all()

        student_list = [('HUG0005', 'Sam', 'Wilson', True),
                        ('WIL0123', 'Jake', 'Bruckner', False),
                        ('ROB2134', 'Ben', 'Hughes', True)]

        for student_id, first_name, last_name, attending in student_list:
            db.session.add(models.Student(student_id=student_id,
                                          first_name=first_name,
                                          last_name=last_name,
                                          attending=attending))

        award_list = [(0, 'Hello World Award', False),
                      (1, 'Very Special Award', True),
                      (2, 'Best Code Testing Award', False)]

        for award_id, award_name, special_award in award_list:
            db.session.add(models.Awards(award_id=award_id,
                                         award_name=award_name,
                                         special_award=special_award))

        award_recipient_list = [(0, 'HUG0005', 1),
                                (1, 'ROB2134', 2),
                                (2, 'WIL0123', 0)]
        for id, student_id, award_id in award_recipient_list:
            db.session.add(models.AwardRecipients(id=id,
                                                  student_id=student_id,
                                                  award_id=award_id))

        db.session.commit()

    def setUp(self):
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

    def test_get_awards(self):
        self.assertEqual(utils.get_awards('ROB2134'), 'Very Special Award')

    @classmethod
    def tearDownClass(cls):
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
