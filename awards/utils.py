from collections import namedtuple
import math
from awards import models, db


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
        return len(models.Student.query.filter_by(year_level=self.year_level).all())

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError('Student index out of range.')
        return models.Student.query.filter_by(year_level=self.year_level).all()[index]

    def get(self, student_id):
        """Get a student via sudent_id.

        Returns None if the student doesn't exist.

        Args:
            student_id: A string of the id of the wanted student.
        """
        return models.Student.query.filter_by(student_id=student_id, year_level=self.year_level).first()

    @property
    def attending(self):
        """A readonly int of the amount of students attending."""
        return len(models.Student.query.filter_by(year_level=self.year_level, attending=True).all())


def group_size(student_count=0):
    """Get the sizes of the award groups.

    Args:
        student_count: An interger of the amount of students attending.
    """
    groups = namedtuple('Groups', ['size', 'count', 'last_size'])
    for group_size in range(7, 10):
        if 10 > (student_count % group_size) > 4 or student_count % group_size == 0:
            groups.size = group_size
            groups.count = math.floor(student_count / group_size)
            groups.last_size = student_count % group_size

    return groups


def get_awards(student_id):
    """Get all the awards for a student.

    Args:
        student_id: A string of the student id to get awards for.
    """

    # TODO: Needs testing
    award_ids = (row.award_id for row in models.AwardRecipients.query.filter_by(student_id=student_id).all())

    return [award.name for award in models.Awards.query.filter_by(award_id=(award_id for award_id in award_ids)).all()]
