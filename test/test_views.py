import unittest
from awards import create_app
from mockdb import MockDB


class TestAttendance(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_attendance(self):
        response = self.app.get('/attendance', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()
        self.md = MockDB()
        self.md.setUp()

    def test_main(self):
        for year_level in self.app.config['YEAR_LEVELS']:
            response = self.test_client.get('/main/{}/0/0'.format(str(year_level)))
            self.assertEqual(response.status_code, 200)

        invalid_year = self.app.config['YEAR_LEVELS'][0] - 1
        response = self.test_client.get('/main/{}/0/0'.format(str(invalid_year)))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.md.tearDown()
