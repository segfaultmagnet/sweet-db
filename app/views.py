# Name:         views.py
# Authors:      Matthew Sheridan
# Date:         22 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

import datetime
import json
import sqlite3

from flask import redirect, render_template, request
from app import app
from jinja2 import Template

from .forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def index():
    empty = True
    sql_request = 'SELECT * FROM entry'
    search = SearchForm()

    if search.event.data:
        sql_request += ' WHERE event_name LIKE \'%' + search.event.data + '%\' COLLATE NOCASE'
        empty = False

    if search.team.data:
        if empty:
            sql_request += ' WHERE'
        else:
            sql_request += ' AND'
        sql_request += ' team_name LIKE \'%' + search.team.data + '%\' COLLATE NOCASE'
        empty = False

    if search.make.data:
        if empty:
            sql_request += ' WHERE'
        else:
            sql_request += ' AND'
        sql_request += ' make LIKE \'%' + search.make.data + '%\' COLLATE NOCASE'
        empty = False

    if search.model.data:
        if empty:
            sql_request += ' WHERE'
        else:
            sql_request += ' AND'
        sql_request += ' model LIKE \'%' + search.model.data + '%\' COLLATE NOCASE'
        empty = False

    sql_request += ' ORDER BY event_date DESC, position ASC'

    db = sqlite3.connect(app.config['ROOT_DIR'] + app.config['SQL_DB'])
    cursor = db.cursor()

    cursor.execute(sql_request)
    result = cursor.fetchall()

    entries = []
    for r in result:
        entries.append({'Position': r[1], 'Team Name': r[2], 'Number': r[3],
                        'Class': r[4], 'Year': r[5], 'Make': r[6],
                        'Model': r[7], 'Laps': r[8], 'Best Time': r[9], 
                        'BS Penalty Laps': r[10], 'Black Flag Laps': r[11],
                        'Event': r[12], 'Date': r[13]})
    db.close()

    return render_template('index.html',
                           title='Poke through the big steaming heap:',
                           search=search,
                           entries=entries)
