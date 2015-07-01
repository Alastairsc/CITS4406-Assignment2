__author__ = 'Liam Jones. http://ljones.id.au. me@ljones.id.au.'

from flask import Flask
from flask_bootstrap import Bootstrap
from .config import config

app = Flask(__name__)
app.config.from_object(config['default'])
Bootstrap(app)

import pystatter.views
