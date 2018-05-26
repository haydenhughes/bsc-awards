import unittest
import sass
import os
from logging.config import dictConfig
from sassutils.wsgi import SassMiddleware
from shutil import copyfile
from flask import Flask
from awards import config, main

'''Flask'''
app = Flask(__name__)
app.config.from_object(config.Config)

# Register blueprints
app.register_blueprint(main.bp)


# TODO: Dont run all tests
@app.cli.command()
def test():
    app.logger.info('Running tests...')
    test_loader = unittest.TestLoader()
    suite = test_loader.discover('test', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)


def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)


'''Sass'''
# FIXME: This is ugly code
# Build Bootstrap
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

app.logger.info('Compiling sass...')
# Build custom Sass on each request
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'awards': ('static/sass', 'static/css', '/static/css')
})
app.logger.info('Done!')
