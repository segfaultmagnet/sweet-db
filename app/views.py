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

from flask import render_template
from app import app
from jinja2 import Template
from operator import attrgetter, itemgetter

@app.route('/')
@app.route('/index')
def index():
    dbpath = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/../json")
    testfile = '11.11.json'
    db = None

    try:
        with open(dbpath + '/' + testfile, 'r') as dat:
            db = json.load(dat)
    except e:
        return render_template('index.html',
                               title='Database Exception')
    eventname = db['Name']
    eventdate = datetime.date(int(db['Date']['Year']),
                              int(db['Date']['Month']),
                              int(db['Date']['Day']))
    
    entries = dict()
    counter = 1
    for item in db.items():
        if str(item[0]) != 'Name' and str(item[0]) != 'Date':
            entries[int(item[0])] = item[1]

    return render_template('index.html',
                           title='sweet-db',
                           eventname=eventname,
                           eventdate=eventdate.strftime('%d %b %Y'),
                           entries=entries)
