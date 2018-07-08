from collections import namedtuple
import math
from awards import db, models


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


class StudentManager:
    """Manages student information.

    Args:
        year_level: A string to specify what year level to work with.
                    None for all (default).
    """

    def __init__(self, year_level=None):
        self.year_level = year_level

    def __enter__(self):
        return self

    def __exit__(self, *args):
        db.session.commit()

    def __len__(self):
        len(models.Student.query.filter_by(attending=True, year_level=self.year_level).all())

    def __iter__(self):
        return iter(models.Student.query.filter_by(attending=True, year_level=self.year_level).all())

    def __getitem__(self, index):
        return models.Student.query.filter_by(student_id=index, year_level=self.year_level).first()
