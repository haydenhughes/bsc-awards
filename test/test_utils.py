import unittest
import random
from awards import utils, models
from mockdb import MockDB


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()
        self.sm = utils.StudentManager()

    def test_get(self):
        self.assertIsNotNone(self.sm.get(
            random.choice(self.mock_db.student_ids)))

    def test_len(self):
        self.assertEqual(len(self.sm), self.mock_db.student_count)

    def test_get_by_index(self):
        index = random.randint(0, self.mock_db.student_count - 1)
        self.assertIsNotNone(self.sm[index])

        with self.assertRaises(IndexError):
            self.sm[self.mock_db.student_count]

    def test_attending(self):
        self.assertEqual(self.sm.attending, self.mock_db.attending_count)

    def tearDown(self):
        self.mock_db.tearDown()


class TestStudentManagerYearRestrictions(TestStudentManager):
    def setUp(self):
        self.mock_db = MockDB([7])
        self.mock_db.setUp()
        self.sm = utils.StudentManager([7])


class TestGetAwards(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()

    def test(self):
        student_id = random.choice(self.mock_db.student_ids)
        awards = [award.award_id for award in models.AwardRecipients.query.filter_by(
            student_id=student_id).all()]
        self.assertCountEqual(
            [award.award_id for award in utils.get_awards(student_id)], awards)

    def tearDown(self):
        self.mock_db.tearDown()


class TestGroupManager(unittest.TestCase):
    def setUp(self):
        self.md = MockDB(student_count=20, year_level=[7])
        self.md.setUp()

        self.gm = utils.GroupManager()

    def test_attributes(self):
        self.assertEqual(self.gm.size, 7)
        self.assertEqual(self.gm.count, 2)
        self.assertEqual(self.gm.last_size, 6)

    def test_get(self):
        self.assertIsNotNone(self.gm[0][0])
        self.assertIsNotNone(self.gm[1][6])

        with self.assertRaises(IndexError):
            self.gm[0][7]

        with self.assertRaises(IndexError):
            self.gm[3][0]

    def tearDown(self):
        self.md.tearDown()
