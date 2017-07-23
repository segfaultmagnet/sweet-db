# Name:         __init__.py
# Authors:      Matthew Sheridan
# Date:         22 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

import os
import json
import sqlite3

from flask import Flask

import util.csvtojson
import util.sqlloader
import util.sweetutils

def _print(msg):
    util.sweetutils._print(__file__, msg)

def _print_warn(msg):
    util.sweetutils._print_warn(__file__, msg)

_debug = True
sql = None

app = Flask(__name__)
app.config.from_object('config')

app.config['ROOT_DIR'] = os.path.normpath(os.path.dirname(__file__) + '/..')

if _debug:
    app.config['DEBUG'] = _debug

if app.config['DEBUG']:
    _print("Running in: " + app.config['ROOT_DIR'])

if app.config['SECRET_KEY'] == 'replace-before-deploying-bEEp-b0oP-#H**ptie_Code(123!)':
    _print_warn('Config value \'SECRET_KEY\' is the default value. Change before deploying!')

if app.config['SQL_DB'] == None or app.config['SQL_DB'] == "":
    app.config['SQL_DB'] = 'temp.db'
    _print_warn('No SQL database specified by config key \'SQL_DB\'\nDefaulting to \'temp.db\'')
_print('Using database \'' + app.config['SQL_DB'] + '\'')

util.csvtojson.main(app.config['DEBUG'])

json_path = os.path.normpath(app.config['ROOT_DIR'] + '/json')
for file in os.listdir(json_path):
    _print("Loading " + str(os.path.basename(file)))
    with open(os.path.normpath(json_path + '/' + file), 'r') as dat:
        db  = sqlite3.connect(app.config['ROOT_DIR'] + app.config['SQL_DB'])
        obj = json.load(dat)
        util.sqlloader.create_table(db)
        util.sqlloader.add_records(obj, db)
        db.close()

from app import views
