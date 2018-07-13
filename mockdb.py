import random
from csv import reader
from awards import create_app, db, models


class MockDB:
    def __init__(self, student_count=60, attending_count=50, recipient_count=80):
        self.student_count = student_count
        self.attending_count = attending_count
        self.recipient_count = recipient_count

        self.student_ids = []
        self.alphabet = [c for c in 'abcdefghijklmnopqrstuvwzyz']

        self.app = create_app()
        self.app.app_context().push()

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

        year_level = random.choice(self.app.config['YEAR_LEVELS'])

        return models.Student(student_id=id,
                              first_name=first_name,
                              last_name=last_name,
                              year_level=year_level,
                              attending=attending)

    def generate_recipient(self, id, student_ids):
        student_id = random.choice(self.student_ids)
        award_id = random.randint(0, self.award_count)
        return models.AwardRecipients(id=id,
                                      student_id=student_id,
                                      award_id=award_id)

    def get_awards(self, csv_file='awards.csv'):
        with open(csv_file) as f:
            csv = reader(f)

            for row in csv:
                id = row[0]
                name = row[1]
                desc = row[2]
                special = row[7]

                yield models.Awards(id=id,
                                    award_name=name,
                                    award_description=desc,
                                    special_award=special)

    def setUp(self):
        db.create_all()

        for num in range(self.student_count):
            db.session.add(self.generate_student(
                num, self.student_ids, self.attending_count))

        for num in range(self.award_count):
            db.session.add(models.Awards(award_id=num))

        for award in self.get_awards():
            db.session.add(award)

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
