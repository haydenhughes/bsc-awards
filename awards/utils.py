from flask import current_app
import math
from awards import models, db
import config


class StudentManager:
    """Manages student information.

    Args:
        year_levels: A array of integers to specify which year levels
                     to work with. None for all (default).
        allow_no_award: A boolean which if True allows for students with no awards
                        to be used. Default: False.
    """

    def __init__(self, year_level=None, allow_no_award=False):
        self.year_levels = config.Config.YEAR_LEVELS
        if year_level is not None:
            self.year_levels = year_level
        self.allow_no_award = allow_no_award

    def __enter__(self):
        return self

    def __exit__(self, *args):
        db.session.commit()

    def __len__(self):
        amount = 0
        for year in self.year_levels:
            for student in models.Student.query.filter_by(year_level=year).all():
                if self._has_awards(student.student_id) or self.allow_no_award:
                    amount += 1

        if amount == 0:
            current_app.logger.error('The Student table has records for \
                                      year {}'.format(year))
        return amount

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError('Student index out of range.')

        for year in self.year_levels:
            if self.allow_no_award:
                return models.Student.query.filter_by(year_level=year).all()[index]
            else:
                return models.Student.query.filter_by(year_level=year, attending=True).all()[index]

    def _has_awards(self, student_id):
        for award in get_awards(student_id):
            if award is not None:
                return True
        return False


    def get(self, student_id):
        """Get a student via sudent_id.

        Returns None if the student doesn't exist.

        Args:
            student_id: A string of the id of the wanted student.

        Returns:
            A models Student object of the wanted student.
        """
        for year in self.year_levels:
            student = models.Student.query.filter_by(student_id=student_id, year_level=year).first()
            if student is not None:
                if self._has_awards(student.student_id) or self.allow_no_award:
                    return student
        return None

    @property
    def attending(self):
        """A readonly int of the amount of students attending."""
        amount = 0
        for year in self.year_levels:
            for student in models.Student.query.filter_by(year_level=year, attending=True).all():
                if self._has_awards(student.student_id) or self.allow_no_award:
                    amount += 1
        return amount


class GroupManager:
    """Work with award groups more easily.

    Args:
        year_level: A array of integers for restricting the groups to a year level.
    """

    def __init__(self, year_level=[7]):
        self.sm = StudentManager(year_level)
        self._attending = self.sm.attending

    def __getitem__(self, index):
        if index < self.count:
            return [self.sm[num] for num in range(self.size * index, (self.size * index) + self.size)]
        elif index == self.count:
            return [self.sm[num] for num in range(self.size * index, (self.size * index) + self.last_size)]

        raise IndexError('Group index out of range.')

    @property
    def size(self):
        """A integer of the size of every group except the last group. ReadOnly.

        If the groups cannot be calculated, then only one group will be greated
        with all the students in it.
        """
        for group_size in range(7, 10):
            if 10 > (self._attending % group_size) > 4 or self._attending % group_size == 0:
                return group_size

        else:
            current_app.logger.warning('Not enough students to create groups. \
                                        Only creating one group.')
            return self._attending

    @property
    def count(self):
        """A integer of amount of groups not including the last group. ReadOnly."""
        if self.size == self._attending:
            return 1

        return math.floor(self._attending / self.size)

    @property
    def last_size(self):
        """A integer of the last group size. ReadOnly.

        To account for 'annoying numbers' (like primes) the size of the last
        group is calculated seperatly to the rest of the groups.
        """
        if self.size == self._attending:
            return 0
        return self._attending % self.size


def get_awards(student_id):
    """A generator that gets all the awards for a student.

    Args:
        student_id: A string of the student id to get awards for.
    """

    for recipient in models.AwardRecipients.query.filter_by(student_id=student_id).all():
        for award in models.Awards.query.filter_by(award_id=recipient.award_id).all():
            if award is None:
                current_app.logger.error('No awards found for student {}'.format(student_id))
            yield award
