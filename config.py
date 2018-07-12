import os


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    YEAR_LEVELS = [7, 8, 9, 10, 11, 12]
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
