from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()


def create_app():
    """Flask app factory."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # TEMP: ErrorView is only for error testing and
    #       should be deleted before merging to staging.
    from awards.views import MainView, AttendanceView, ErrorView
    MainView.register(app)
    AttendanceView.register(app)
    ErrorView.register(app)

    return app
