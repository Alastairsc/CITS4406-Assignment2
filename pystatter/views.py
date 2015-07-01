__author__ = 'Liam Jones. http://ljones.id.au. me@ljones.id.au.'

import os

from pystatter import app
from flask import render_template

log_dir = app.config.get('CSV_DIR')


@app.route('/')
def index():
    files = [file for file in os.listdir(log_dir)]
    return render_template('index.html', files=files)
