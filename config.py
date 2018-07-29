import os


class Config:
    NAVBAR_BRAND = 'BSC Awards'
    ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
    YEAR_LEVELS = [7, 8, 9, 10, 11, 12]
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
