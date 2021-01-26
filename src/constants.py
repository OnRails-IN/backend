import os
import yaml

ENV = os.environ.get("PYTHON_ENV")

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
	config = yaml.load(file, Loader = yaml.Loader)[ENV]

SECRET_KEY = config['SECRET_KEY']
DOMAIN = config['DOMAIN']
ES_URI = config['ES_URI']
REDIS_HOST = config['REDIS_HOST']
REDIS_PORT = config['REDIS_PORT']
REDIS_PASSWORD = config['REDIS_PASSWORD']