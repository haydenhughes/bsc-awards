class Config:
    FLASK_APP = 'awards'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@db/user'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@postgres/postgres'
    TESTING = True
