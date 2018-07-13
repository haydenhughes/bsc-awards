import random
from csv import reader
from awards import create_app, db, models


class MockDB:
    def __init__(self, student_count=60, attending_count=50, recipient_count=80):
        self.student_count = student_count
        self.attending_count = attending_count
        self.recipient_count = recipient_count

        self.student_ids = []
        self.alphabet = [c for c in 'abcdefghijklmnopqrstuvwxyz']

        self.app = create_app()
        self.app.app_context().push()

        self.award_count = 0

    def __enter__(self):
        self.setUp()
        return self

    def __exit__(self, *args):
        self.tearDown()

    def generate_name(self, min_length=3, max_length=8):
        length = random.randint(min_length, max_length)
        return ''.join(random.choices(self.alphabet, k=length))

    def generate_student(self, index):
        id_str = self.generate_name(3, 3).upper()
        id_int = random.randint(0, 999)
        if id_int < 100:
            id = '{}0{}'.format(id_str, str(id_int))
        elif id_int < 10:
            id = '{}00{}'.format(id_str, str(id_int))
        else:
            id = id_str + str(id_int)

        self.student_ids.append(id)

        first_name = self.generate_name().capitalize()
        last_name = self.generate_name().capitalize()

        attending = False

        if index < self.attending_count:
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
                # HACK: Alright with this data set as there isn't any special
                #       awards.
                special = False

                self.award_count += 1

                yield models.Awards(award_id=id,
                                    award_name=name,
                                    award_description=desc,
                                    special_award=special)

    def setUp(self):
        db.create_all()

        for num in range(self.student_count):
            db.session.add(self.generate_student(num))

        for award in self.get_awards():
            db.session.add(award)

        for num in range(self.recipient_count):
            db.session.add(self.generate_recipient(num, self.student_ids))

        db.session.commit()

    def tearDown(self):
        models.Student.query.delete()
        models.Awards.query.delete()
        models.AwardRecipients.query.delete()
        db.session.commit()


if __name__ == '__main__':
    mockdb = MockDB()
    mockdb.tearDown()
    mockdb.setUp()
    print('Done!')
