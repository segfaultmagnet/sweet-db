# Name:         sqlloader.py
# Authors:      Matthew Sheridan
# Date:         22 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

import datetime

import util.sweetutils

def _print(msg):
    util.sweetutils._print(__file__, msg)

def _print_raw(msg):
    util.sweetutils._print_raw(__file__, msg)

def _print_warn(msg):
    util.sweetutils._print_warn(__file__, msg)

def add_records(obj, db):
    """
    @param obj = JSON object
    @param db  = SQL database
    """

    entries = dict()
    for o in obj.items():
        if str(o[0]) != 'Name' and str(o[0]) != 'Date':
            entries[int(o[0])] = o[1]

    for e in entries.items():
        e[1]['Event']    = str(obj['Name'])
        e[1]['Date']     = datetime.date(int(obj['Date']['Year']),
                                         int(obj['Date']['Month']),
                                         int(obj['Date']['Day']))
        e[1]['Position'] = e[0]

    cursor = db.cursor()
    for e in entries.items():
        cursor.execute("INSERT OR IGNORE INTO entry VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (e[1]['Hash'], e[1]['Position'], e[1]['Team Name'],
                       e[1]['Number'], e[1]['Class'], e[1]['Year'],
                       e[1]['Make'], e[1]['Model'], e[1]['Laps'],
                       e[1]['Best Time'], e[1]['BS Penalty Laps'],
                       e[1]['Black Flag Laps'], e[1]['Event'], e[1]['Date']))
        db.commit()

def create_table(db):
    cursor = db.cursor()
    command = """
    CREATE TABLE IF NOT EXISTS entry (
    record_number int PRIMARY KEY,
    hash BLOB,
    position int,
    team_name text,
    vic_no int,
    class CHAR(1),
    year int,
    make text,
    model text,
    laps int,
    best_time text,
    bs_laps int,
    flag_laps int,
    event_name text,
    event_date text,
    UNIQUE (hash));
    """
    cursor.execute(command)
    db.commit()
