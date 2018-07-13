import random
from awards import create_app, db, models


class MockDB:
    def __init__(self, student_count=60, attending_count=50, award_count=5, recipient_count=80):
        self.student_count = student_count
        self.attending_count = attending_count
        self.award_count = award_count
        self.recipient_count = recipient_count

        self.student_ids = []
        self.alphabet = [c for c in 'abcdefghijklmnopqrstuvwzyz']

        app = create_app()
        app.app_context().push()

    def __enter__(self):
        self.setUp()
        return self

    def __exit__(self, *args):
        self.tearDown()

    def generate_name(self, min_length=3, max_length=8):
        length = random.randrange(min_length, max_length)
        return ''.join(random.choices(self.alphabet, k=length))

    def generate_student(self, index, student_ids, attending_count):
        id = '{}{}'.format(self.generate_name(3, 3).upper(), str(random.randint(0, 999)))
        student_ids.append(id)

        first_name = self.generate_name()
        last_name = self.generate_name()

        attending = False

        if index < attending_count:
            attending = True

        return models.Student(student_id=id,
                              first_name=first_name,
                              last_name=last_name,
                              attending=attending)

    def generate_recipient(self, id, student_ids):
        student_id = random.choice(self.student_ids)
        award_id = random.randint(0, self.award_count)
        return models.AwardRecipients(id=id,
                                      student_id=student_id,
                                      award_id=award_id)

    def setUp(self):
        db.create_all()

        for num in range(self.student_count):
            db.session.add(self.generate_student(
                num, self.student_ids, self.attending_count))

        for num in range(self.award_count):
            db.session.add(models.Awards(award_id=num))

        for num in range(self.recipient_count):
            db.session.add(self.generate_recipient(num, self.student_ids))

        db.session.commit()

    def tearDown(self):
        models.Student.query.delete()
        models.Awards.query.delete()
        models.AwardRecipients.query.delete()
        db.session.commit()


if __name__ == '__main__':
    MockDB().tearDown()
    MockDB().setUp()
    print('Done!')
