from awards import db
from flask import current_app


class AwardRecipients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(7), nullable=False)
    award_id = db.Column(db.Integer, nullable=False)


class Student(db.Model):
    student_id = db.Column(db.String(7), primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    preferred_name = db.Column(db.String(120))
    year_level = db.Column(db.Integer)
    form_group = db.Column(db.String(3))
    house = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    address = db.Column(db.String(120))
    suburb = db.Column(db.String(120))
    postcode = db.Column(db.String(4))
    primary_parent = db.Column(db.String(120))
    attending = db.Column(db.Boolean, nullable=False)

    def awards(self):
        """A generator that gets all the awards for a student."""
        for recipient in AwardRecipients.query.filter_by(student_id=self.student_id).all():
            for award in Awards.query.filter_by(award_id=recipient.award_id, special_award=False).all():
                if award is None:
                    current_app.logger.error(
                        'No awards found for student {}'.format(self.student_id))
                yield award

    @property
    def has_awards(self):
        """A readonly boolean of whether the student will receive an award"""
        if len(list(self.awards())) != 0:
            return True
        return False

    @property
    def full_name(self):
        """Readonly string of student's full name accounting for prefered names"""
        if self.preferred_name is not None:
            return'{} {}'.format(
                self.preferred_name, self.last_name)
        return '{} {}'.format(self.first_name, self.last_name)


class Awards(db.Model):
    award_id = db.Column(db.Integer, primary_key=True)
    award_name = db.Column(db.String(120))
    award_description = db.Column(db.String(120))
    award_certificate_title = db.Column(db.String(120))
    award_certificate_title_1 = db.Column(db.String(120))
    award_certificate_title_2 = db.Column(db.String(120))
    award_certificate_title_3 = db.Column(db.String(120))
    award_certificate_sub_title = db.Column(db.String(120))
    special_award = db.Column(db.Boolean)
    number_of_awards = db.Column(db.Integer)
    prize = db.Column(db.String(120))
