import argparse
from config import *
from awards import create_app

parser = argparse.ArgumentParser(description='Run the server.')
parser.add_argument('--config', type=str,
                    help='a object in config.py')

args = parser.parse_args()

app = create_app(eval(args.config))

app.run(host='0.0.0.0', port=5000)
