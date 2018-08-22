import random
from csv import reader
from awards import create_app, db, models


class MockDB:
    """Fill a database with dummy values for testing.

    MockDB uses the database configuration from config.py

    Args:
        year_level: A list of year levels (int) to create dummy data for.
                    None uses the year_level variable in config.py (default).

        student_count: A integer for the amount of students to create.
                       Default 60.

        attending_count: A integer of amount of students attending. Default 50.

        recipient_count: A interger of the amount of award AwardRecipients
                         to create. Default 80.
    """

    def __init__(self, year_levels=None, student_count=60, attending_count=50, recipient_count=80):
        self.student_count = student_count
        self.attending_count = attending_count
        self.recipient_count = recipient_count

        self.student_ids = []
        self._alphabet = [c for c in 'abcdefghijklmnopqrstuvwxyz']

        self._app = create_app()
        self._app.app_context().push()

        self.year_levels = year_levels
        if year_levels is None:
            self.year_levels = self._app.config['YEAR_LEVELS']

        self.award_count = 0

    def __enter__(self):
        self.setUp()
        return self

    def __exit__(self, *args):
        self.tearDown()

    def generate_name(self, min_length=3, max_length=8):
        """Generate a random name of random length.

        Args:
            min_length: A integer of the minimum character length of the name.

            max_length: A interger of the maximum character length of the name.

        Returns:
            A string of the generated name.
        """
        length = random.randint(min_length, max_length)
        return ''.join(random.choices(self._alphabet, k=length))

    def generate_student(self, index):
        """Generates a models.Student object.

        Includes a random first_name, last_name, year_level, form groups
        and attending

        Args:
            index: A integer of the amount of students created. Used to workout
                   if the student should be attending or not.

        Returns:
            A models.Student object as well as populating self.student_ids.
        """
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

        if random.choice([True, False, False, False]):
            preferred_name = self.generate_name().capitalize()
        else:
            preferred_name = None

        attending = False

        if index < self.attending_count:
            attending = True

        year_level = random.choice(self.year_levels)

        form_group = random.choice(
            self._alphabet).upper() + str(random.randint(1, 15))

        return models.Student(student_id=id,
                              first_name=first_name,
                              last_name=last_name,
                              preferred_name=preferred_name,
                              year_level=year_level,
                              form_group=form_group,
                              attending=attending)

    def generate_recipient(self, id, student_id):
        """Generates a models.AwardRecipients object.

        Args:
            id: An integer of the id (the primary key for the database)
                of the object.

        Returns:
            A models.AwardRecipients object.
        """
        award_id = random.randint(0, self.award_count)
        return models.AwardRecipients(id=id,
                                      student_id=student_id,
                                      award_id=award_id)

    def get_awards(self, csv_file='awards.csv'):
        """A generator method for getting models.Awards objects.

        get_awards reads a csv file to collect the award information.
        See awards.csv for an example.

        Args:
            csv_file: A string of a csv file to read from.

        Returns:
            A generator of models.Awards objects.
        """
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
        """Creates and populates the database tables."""
        db.create_all()

        for num in range(self.student_count):
            db.session.add(self.generate_student(num))

        for award in self.get_awards():
            db.session.add(award)

        for num in range(self.student_count):
            db.session.add(self.generate_recipient(num, self.student_ids[num]))

        db.session.commit()

    def tearDown(self):
        """Deletes the created database tables"""
        models.Student.query.delete()
        models.Awards.query.delete()
        models.AwardRecipients.query.delete()
        db.session.commit()


if __name__ == '__main__':
    # TODO: Add argparse support
    mockdb = MockDB()

    # HACK: If the tables do not exist then they connot be deleted
    try:
        mockdb.tearDown()
    except Exception as e:
        pass

    mockdb.setUp()

    print('Done!')
    print()
    print('Generated student IDs:')
    print(mockdb.student_ids)
