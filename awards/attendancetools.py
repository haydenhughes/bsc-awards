from awards import db, models


class AttendanceTracker:
    """A helper object for managing student attendance."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        db.session.commit()

    def __iter__(self):
        return iter(models.Student.query.filter_by(attending=True).all())

    def __getitem__(self, index):
        return models.Student.query.filter_by(student_id=index).first()
