from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore


db = SQLAlchemy()


def create_app():
    """Flask app factory."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from awards.views import MainView, AttendanceView
    MainView.register(app)
    AttendanceView.register(app)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error/500.html'), 500

    # Setup Flask-Security
    from awards.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @app.before_first_request
    def create_user(email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASSWORD']):
        db.create_all()
        user_datastore.create_user(email=email, password=password)
        db.session.commit()

    return app
