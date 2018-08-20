import unittest
from awards import utils, models
from mockdb import MockDB


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()
        self.sm = utils.StudentManager(allow_no_award=True)

    def test_get(self):
        for student_id in self.mock_db.student_ids:
            self.assertIsNotNone(self.sm.get(student_id))

    def test_len(self):
        self.assertEqual(len(self.sm), self.mock_db.student_count)

    def test_get_by_index(self):
        for student in self.sm:
            self.assertIsNotNone(student)

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
        self.sm = utils.StudentManager([7], allow_no_award=True)

class TestGetAwards(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()

    def test(self):
        for student_id in self.mock_db.student_ids:
            awards = [award.award_id for award in models.AwardRecipients.query.filter_by(
                student_id=student_id).all()]
            self.assertCountEqual(list(utils.get_awards(student_id)), awards)

    def tearDown(self):
        self.mock_db.tearDown()

