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
        entries.append({'Position': r[1], 'Team Name': r[2], 'Number': r[3],
                        'Class': r[4], 'Year': r[5], 'Make': r[6],
                        'Model': r[7], 'Laps': r[8], 'Best Time': r[9], 
                        'BS Penalty Laps': r[10], 'Black Flag Laps': r[11],
                        'Event': r[12], 'Date': r[13]})

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
