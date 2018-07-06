import os


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    YEAR_LEVELS = ['Year 7', 'Year 8', 'Year 9',
                   'Year 10', 'Year 11', 'Year 12']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
