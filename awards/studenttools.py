from awards import db, models


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

    def __iter__(self):
        return iter(models.Student.query.filter_by(attending=True, year_level=self.year_level).all())

    def __getitem__(self, index):
        return models.Student.query.filter_by(student_id=index, year_level=self.year_level).first()
