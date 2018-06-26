import unittest
from awards import create_app


class TestViews(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_attendance(self):
        response = self.app.get('/attendance', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
