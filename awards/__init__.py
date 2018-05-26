import unittest
import sass
import os
import logging
from sassutils.wsgi import SassMiddleware
from shutil import copyfile
from flask import Flask
from awards import config, main

# TODO: Test The logging config (I think it needs to
#       use app.logger.config.dictConfig)
'''Logging'''
logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

'''Flask'''
app = Flask(__name__)
app.config.from_object(config.Config)

# Register blueprints
app.register_blueprint(main.bp)


# TODO: Dont run all tests
@app.cli.command()
def test():
    logging.info('Running tests...')
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
copyfile(get_path('node_modules/bootstrap/dist/js/bootstrap.min.js'),
         get_path('static/js/bootstrap.min.js'))
copyfile(get_path('node_modules/jquery/dist/jquery.min.js'),
         get_path('static/js/query.min.js'))
copyfile(get_path('node_modules/popper.js/dist/umd/popper.min.js'),
         get_path('static/js/popper.min.js'))
app.logger.info('Done!')

logging.info('Compiling sass...')
# Build custom Sass on each request
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'awards': ('static/sass', 'static/css', '/static/css')
})
app.logger.info('Done!')
