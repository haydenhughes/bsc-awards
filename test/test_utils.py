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


class TestGroupManager:
    def setUp(self):
        self.mock_db = MockDB()
        self.mock_db.setUp()
        self.g = utils.GroupManager()
        self.g.sm.allow_no_award = True
        self.g._attending = 52

    def test_index(self):
        for student_list in self.g[0]:
            for student in student_list:
                self.assertIsNotNone(student)

        with self.assertRaises(IndexError):
            self.g[self.mockdb.student_count]

    def test_size(self):
        self.assertEqual(self.g.size, 9)

    def test_count(self):
        self.assertEqual(self.g.count, 5)

    def test_last_size(self):
        self.assertEqual(self.g.last_size, 7)

    def tearDown(self):
        self.mock_db.tearDown()
