import os


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    YEAR_LEVELS = ['year_7', 'year_8', 'year_9',
                   'year_10', 'year_11', 'year_12']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
