import os


class Config:
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SECURITY_PASSWORD_SALT = 'change-me-as-well'
    NAVBAR_BRAND = 'BSC Awards'

    YEAR_LEVELS = [7, 8, 9, 10, 11, 12]
    CSRF_ENABLED = True

    ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
