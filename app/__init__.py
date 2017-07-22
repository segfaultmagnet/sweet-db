# Name:         __init__.py
# Authors:      Matthew Sheridan
# Date:         22 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

import os
from flask import Flask

_debug = True

app = Flask(__name__)
app.config.from_object('config')
app.config['root_dir'] = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/..")
if _debug:
    app.config['DEBUG'] = _debug

if app.config['DEBUG']:
    print("Running in: " + app.config['root_dir'])

if app.config['SECRET_KEY'] == 'replace-before-deploying-bEEp-b0oP-#H**ptie_Code(123!)':
    print('WARNING: Config value SECRET_KEY is the default value. Change before deploying!')


from app import views
