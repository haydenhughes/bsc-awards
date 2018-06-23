class Config:
    FLASK_APP = 'awards'
    SQLALCHEMY_DATABASE_URI = 'postgres://user:pass@db/user'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:pass@db/postgres'
    TESTING = True
