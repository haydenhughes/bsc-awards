import unittest
from awards import create_app


class TestFlask(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
