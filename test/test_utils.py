import unittest
import random
from awards import models, db, create_app, utils


class TestDB(unittest.TestCase):
    @classmethod
    def setUp(self):
        # OPTIMIZE: Does not need to recreate everything every test. Although
        # the tests need access to student_ids.
        self.student_count = 60
        self.attending_count = 50
        award_count = 5
        recipient_count = 80

        self.student_ids = []

        def generate_student(index, student_ids, attending_count):
            id = ''
            for num in range(3):
                # HACK: There must be a better way
                id += random.choice(['A', 'B', 'C', 'D'])

            id += str(random.randint(0, 999))

            student_ids.append(id)

            attending = False

            if index < attending_count:
                attending = True

            return models.Student(student_id=id, attending=attending)

        def generate_recipient(id, student_ids):
            student_id = random.choice(student_ids)
            award_id = random.randint(0, award_count)
            return models.AwardRecipients(id=id,
                                          student_id=student_id,
                                          award_id=award_id)

        app = create_app()
        app.app_context().push()

        db.create_all()

        for num in range(self.student_count):
            db.session.add(generate_student(
                num, self.student_ids, self.attending_count))

        for num in range(award_count):
            db.session.add(models.Awards(award_id=num))

        for num in range(recipient_count):
            db.session.add(generate_recipient(num, self.student_ids))

        db.session.commit()

        self.sm = utils.StudentManager()

    def test_StudentManager_get(self):
        self.assertIsNotNone(self.sm.get(random.choice(self.student_ids)))

    def test_StudentManager_len(self):
        self.assertEqual(len(self.sm), self.student_count)

    def test_StudentManager_get_by_index(self):
        index = random.randrange(0, self.student_count)

        self.assertEqual(self.sm[index].student_id, self.student_ids[index])

        with self.assertRaises(IndexError):
            self.sm[self.student_count]

    def test_StudentManager_attending(self):
        self.assertEqual(self.sm.attending, self.attending_count)

    def test_get_awards(self):
        student_id = random.choice(self.student_ids)
        awards = [award.award_id for award in models.AwardRecipients.query.filter_by(student_id=student_id).all()]
        self.assertCountEqual([award.award_id for award in utils.get_awards(student_id)], awards)

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
