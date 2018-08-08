import unittest
import random
from awards import create_app, utils
from mockdb import MockDB


class TestAttendance(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.post('/login/', data=dict(
                         username=self.app.config['USERNAME'],
                         password=self.app.config['PASSWORD']
                         ), follow_redirects=True)

        self.md = MockDB()
        self.md.setUp()
        self.sm = utils.StudentManager()

    def test_url(self):
        response = self.client.get('/attendance', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_student_search(self):
        student_id = random.choice(self.md.student_ids)
        student = self.sm.get(student_id)
        rv = self.client.get('/attendance?studentID={}'.format(student_id), follow_redirects=True)

        self.assertTrue(str.encode('{} {}'.format(student.first_name, student.last_name)) in rv.data)

    def tearDown(self):
        self.md.tearDown()


class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.post('/login/', data=dict(
                         username=self.app.config['USERNAME'],
                         password=self.app.config['PASSWORD']
                         ), follow_redirects=True)
        self.md = MockDB()
        self.md.setUp()

    def test_main(self):
        for year_level in self.app.config['YEAR_LEVELS']:
            response = self.client.get('/main/{}/0/0'.format(str(year_level)), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        invalid_year = self.app.config['YEAR_LEVELS'][0] - 1
        response = self.client.get('/main/{}/0/0'.format(str(invalid_year)), follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.md.tearDown()


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.md = MockDB()
        self.md.setUp()

    def test_login(self):
        rv = self.client.post('/login/', data=dict(
                              username=self.app.config['USERNAME'],
                              password=self.app.config['PASSWORD']
                              ), follow_redirects=True)
        self.assertNotIn(b'Incorrect username or password.', rv.data)

    def test_failed_login(self):
        rv = self.client.post('/login/', data=dict(
                              username=self.app.config['USERNAME'] + 'x',
                              password=self.app.config['PASSWORD']
                              ), follow_redirects=True)
        self.assertIn(b'Incorrect username or password.', rv.data)

        rv = self.client.post('/login/', data=dict(
                              username=self.app.config['USERNAME'],
                              password=self.app.config['PASSWORD'] + 'x'
                              ), follow_redirects=True)
        self.assertIn(b'Incorrect username or password.', rv.data)

    def test_logout(self):
        self.client.post('/login/', data=dict(
                         username=self.app.config['USERNAME'],
                         password=self.app.config['PASSWORD']
                         ), follow_redirects=True)

        rv = self.client.get('/logout/', follow_redirects=True)
        self.assertIn(b'Logged out.', rv.data)

    def tearDown(self):
        self.md.tearDown()
