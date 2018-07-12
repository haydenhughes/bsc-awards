from awards import db


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
    form_group = db.Column(db.String(2))
    house = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    address = db.Column(db.String(120))
    suburb = db.Column(db.String(120))
    postcode = db.Column(db.String(4))
    primary_parent = db.Column(db.String(120))
    attending = db.Column(db.Boolean, nullable=False)


class Awards(db.Model):
    award_id = db.Column(db.Integer, primary_key=True)
    award_name = db.Column(db.String(120))
    award_desription = db.Column(db.String(120))
    award_certificate_title = db.Column(db.String(120))
    award_certificate_title_1 = db.Column(db.String(120))
    award_certificate_title_2 = db.Column(db.String(120))
    award_certificate_title_3 = db.Column(db.String(120))
    award_certificate_sub_title = db.Column(db.String(120))
    special_award = db.Column(db.Boolean)
    number_of_awards = db.Column(db.Integer)
    prize = db.Column(db.String(120))
