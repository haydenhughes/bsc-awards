from awards import db, models


class AttendanceTracker:
    """A helper object for managing student attendance."""

    def _get_student(self, student_id):
        return models.Student.query.filter_by(student_id=student_id).first()

    def __iter__(self):
        return iter(models.Student.query.filter_by(attending=True).all())

    def __getitem__(self, index):
        return self._get_student(index).attending

    def __setitem__(self, index, value):
        student = self._get_student(index)
        student.attending = value
        db.session.commit()
