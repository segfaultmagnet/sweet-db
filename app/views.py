# Name:         views.py
# Authors:      Matthew Sheridan
# Date:         22 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

import os
import sys
import datetime
import json
import sqlite3
from operator import attrgetter, itemgetter

from flask import render_template
from app import app
from jinja2 import Template

@app.route('/')
@app.route('/index')
def index():
    db = sqlite3.connect(app.config['ROOT_DIR'] + app.config['SQL_DB'])
    cursor = db.cursor()

    cursor.execute("SELECT * FROM entry ORDER BY event_date DESC, position ASC")
    result = cursor.fetchall()

    entries = []
    for r in result:
        entries.append({'Position': r[2], 'Team Name': r[3], 'Number': r[4],
                        'Class': r[5], 'Year': r[6], 'Make': r[7],
                        'Model': r[8], 'Laps': r[9], 'Best Time': r[10], 
                        'BS Penalty Laps': r[11], 'Black Flag Laps': r[12],
                        'Event': r[13], 'Date': r[14]})

    db.close()

    eventname = None
    eventdate = None

    if eventname and eventdate:
        eventname += ' (' + eventdate.strftime('%d %b %Y') + ')'

    return render_template('index.html',
                           title='All Race Results in a Big Steaming Heap',
                           eventname=eventname,
                           eventdate=eventdate, #.strftime('%d %b %Y'),
                           entries=entries)
