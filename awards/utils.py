from collections import namedtuple
import math
from awards import db


class Utils:
    """Random helper methods."""

    @staticmethod
    def group_size(student_count=0):
        """Get the sizes of the award groups.

        Args:
            student_count: An interger of the amount of students attending.
        """
        groups = namedtuple('Groups', ['size', 'amount', 'last_size'])
        for group_size in range(7, 10):
            if 10 > (student_count % group_size) > 4 or student_count % group_size == 0:
                groups.size = group_size
                groups.count = math.floor(student_count / group_size)
                groups.last_size = student_count % group_size
        return groups
