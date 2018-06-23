from test import db_testcase


class TestAttentanceTracker(db_testcase.DBTestCase):
    def test_get(self):
        self.assertTrue(self.attendance_tracker['HUG0005'])
        self.assertFalse(self.attendance_tracker['WIL0123'])

    def test_set(self):
        self.attendance_tracker['ROB2134'] = False
        self.assertFalse(self.attendance_tracker['ROB2134'])

    def test_iter(self):
        students = [student_id for student_id in self.attendance_tracker]
        self.assertEqual(len(students), 3)
