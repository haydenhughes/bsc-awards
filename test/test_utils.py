import unittest
import random
from awards import utils, models
from mockdb import MockDB


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()
        self.sm = utils.StudentManager()

    def test_StudentManager_get(self):
        self.assertIsNotNone(self.sm.get(random.choice(self.mock_db.student_ids)))

    def test_StudentManager_len(self):
        self.assertEqual(len(self.sm), self.mock_db.student_count)

    def test_StudentManager_get_by_index(self):
        index = random.randrange(0, self.mock_db.student_count)

        self.assertEqual(self.sm[index].student_id, self.mock_db.student_ids[index])

        with self.assertRaises(IndexError):
            self.sm[self.mock_db.student_count]

    def test_StudentManager_attending(self):
        self.assertEqual(self.sm.attending, self.mock_db.attending_count)

    def tearDown(self):
        self.mock_db.tearDown()


class TestGetAwards(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()

    def test(self):
        student_id = random.choice(self.mock_db.student_ids)
        awards = [award.award_id for award in models.AwardRecipients.query.filter_by(student_id=student_id).all()]
        self.assertCountEqual([award.award_id for award in utils.get_awards(student_id)], awards)

    def tearDown(self):
        self.mock_db.tearDown()


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
