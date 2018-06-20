import sass
import os
from flask_sqlalchemy import SQLAlchemy
from sassutils.wsgi import SassMiddleware
from shutil import copyfile
from flask import Flask

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    from awards import main
    app.register_blueprint(main.bp)

    def get_path(path):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, path)

    app.logger.info('Compiling Bootstrap...')

    sass.compile(
        dirname=(get_path('node_modules/bootstrap/scss/'), get_path('static/css')))

    if not os.path.exists(get_path('static/css')):
        os.makedirs(get_path('static/css'))
    if not os.path.exists(get_path('static/js')):
        os.makedirs(get_path('static/js'))

    copyfile(get_path('node_modules/bootstrap/dist/js/bootstrap.min.js'),
             get_path('static/js/bootstrap.min.js'))
    copyfile(get_path('node_modules/jquery/dist/jquery.min.js'),
             get_path('static/js/query.min.js'))
    copyfile(get_path('node_modules/popper.js/dist/umd/popper.min.js'),
             get_path('static/js/popper.min.js'))

    app.logger.info('Done!')

    app.logger.info('Compiling sass for the first time...')

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'awards': ('static/sass', 'static/css', '/static/css')
    })

    return app
