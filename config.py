import os


class Config:
    SECRET_KEY = os.urandom(12)
    NAVBAR_BRAND = 'BSC Awards'

    YEAR_LEVELS = [7, 8, 9, 10, 11, 12]
    CSRF_ENABLED = True

    USERNAME = os.environ['AWARDS_USERNAME']
    PASSWORD = os.environ['AWARDS_PASSWORD']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
