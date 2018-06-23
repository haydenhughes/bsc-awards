import unittest
from awards import create_app
from config import Testing


class TestFlask(unittest.TestCase):
    def setUp(self):
        app = create_app(Testing)
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
