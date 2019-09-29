import os


class Config:
    SECRET_KEY = os.urandom(12)
    NAVBAR_BRAND = 'BSC Awards'

    YEAR_LEVELS = [7, 8, 9, 10, 11, 12]
    CSRF_ENABLED = True

    USERNAME = os.getenv('AWARDS_USERNAME', 'admin')
    PASSWORD = os.getenv('AWARDS_PASSWORD', 'admin')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///data.db')
