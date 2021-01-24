import os
import yaml

ENV = os.environ.get("PYTHON_ENV")

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
	config = yaml.load(file, Loader = yaml.Loader)[ENV]

DOMAIN = config['DOMAIN']
ES_URI = config['ES_URI']