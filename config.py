class Config:
    FLASK_APP = 'awards'
    SQLALCHEMY_DATABASE_URI = 'postgres:////user:pass@db/user'


class Development(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    TESTING = True
