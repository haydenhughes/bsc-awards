from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

db = SQLAlchemy()


def create_app():
    """Flask app factory."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from awards.views import MainView, AttendanceView, LoginView, LogoutView, IndexView
    MainView.register(app)
    AttendanceView.register(app)
    LoginView.register(app)
    LogoutView.register(app)
    IndexView.register(app)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error/500.html'), 500

    return app

