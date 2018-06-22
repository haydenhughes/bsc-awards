import unittest
from awards.utils import Utils


class TestUtils(unittest.TestCase):
    def test_group_size(self):
        self.assertEqual(Utils.group_size(60).size, 9)
        self.assertEqual(Utils.group_size(60).amount, 6)
        self.assertEqual(Utils.group_size(60).last_group_size, 6)

        self.assertEqual(Utils.group_size(49).size, 7)
        self.assertEqual(Utils.group_size(49).amount, 7)
        self.assertEqual(Utils.group_size(49).last_group_size, 0)

        self.assertEqual(Utils.group_size(75).size, 7)
        self.assertEqual(Utils.group_size(75).amount, 10)
        self.assertEqual(Utils.group_size(75).last_group_size, 5)

        self.assertEqual(Utils.group_size(51).size, 9)
        self.assertEqual(Utils.group_size(51).amount, 5)
        self.assertEqual(Utils.group_size(51).last_group_size, 6)
