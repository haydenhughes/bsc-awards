from awards import db
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


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
