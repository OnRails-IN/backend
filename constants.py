import os

ENV = os.environ.get("PYTHON_ENV")

INDEX_KEYS = {
    'a':'Amelie', 'b':'Basterds', 'c':'Corleone', 'd':'Django', 'e':'Edgar',
    'f':'Floorgang', 'g':'Gandalf', 'h':'HansLanda', 'i':'Ireland', 'j':'Jeeves',
    'k':'Kubrick', 'l':'Lebowski', 'm':'Masterpiece', 'n':'Norman', 'o':'Ozymandias',
    'p':'Pikachu', 'q':'Quasimodo', 'r':'Reddit', 's':'Strangelove', 't':'Tambourine',
    'u':'Updog', 'v':'Vader', 'w':'Waffles', 'x':'Xenon', 'y':'Yoda', 'z':'Zulu'
}

SECRET_KEY = os.environ.get('SECRET_KEY')

DOMAIN = os.environ.get('DOMAIN')

ES_URI = os.environ.get('ES_URI')

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

DYNAMO_URL = os.environ.get('DYNAMO_URL')