from collections import namedtuple
import math


class Utils:
    """Random helper methods."""

    @staticmethod
    def group_size(student_count=0):
        """Get the sizes of the award groups.

        Args:
            student_count: An interger of the amount of students attending.
        """
        output = namedtuple('Group_Size', ['size', 'amount', 'last_group_size'])
        for group_size in range(7, 10):
            if 10 > (student_count % group_size) > 4 or student_count % group_size == 0:
                output.size = group_size
                output.amount = math.floor(student_count / group_size)
                output.last_group_size = student_count % group_size

        return output
