#!/usr/bin/env python3

# Name:         csvtojson.py
# Authors:      Matthew Sheridan
# Date:         21 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

"""Usage:
  csvtojson.py [-d]
  csvtojson.py -h | --help
  csvtojson.py -v | --version

Arguments:
  input     Reads CSV files which contain LeMons race results and converts
            them to a JSON format.

            It is assumed that:
              input files are in:        "/csv"
              output files will be in:   "/json"

            All CSV files within the input directory will be processed and
            their filenames used for the resulting output JSON files. Output
            files will be overwritten if they already exist.

            Example:
              "/csv/hooptiefest2017.csv"
            Will be processed into:
              "/json/hooptiefest2017.json"


Options:
  -d             Enable debugging output.
  -h --help      Show this help message.
  -v, --version  Display program version number.
"""

__author__  = "Matthew Sheridan"
__credits__ = ["Matthew Sheridan"]
__date__    = "22 July 2017"
__version__ = "0.1"
__status__  = "Development"

import os
import sys
import csv
import json
from docopt import docopt

class _Error(Exception):
    """Base class for error handling."""
    def __init__(self, msg):
        self._msg = msg
    def __str__(self):
        return repr(type(self).__name__ + ": " + self._msg)

class _InputFileError(_Error):
    """Should be thrown for any problematic input files."""
    def __init__(self, file):
        self._msg = "Failed to parse file: " + repr(file)

class _OutputFileError(_Error):
    """Should be thrown for any problematic output files."""
    def __init__(self, file):
        self._msg = "Failed to write out file: " + repr(file)

class _HooptieError(_Error):
    """Our hooptie has crashed and burned!"""
    def __init__(self, file, errorcode):
        self._msg = "Error " + repr(errorcode) + ": our hooptie has crashed and burned!"

def _convert(input_path, output_path):
    """
    @param input_path:  CSV containing race results.
    @param output_path: JSON file to store re-formatted results.

    Returns:
        0:  success
        1:  problematic input
        2:  problematic output
        -1: crazy catch-all for fatal errors
    """
    try:
        entry_count = 0
        with open(input_path, "r") as in_file:
            reader = csv.reader(in_file, delimiter=',', quotechar='|')

            race_name = str(next(reader)[0])
            date  = next(reader) # This line contains day, month, and year.
            day   = str(date[1])
            month = str(date[0])
            year  = str(date[2])
            meta_string = '"Name": "' + race_name      \
                        + '", "Date": {"Day": ' + day \
                        + ', "Month": ' + month       \
                        + ', "Year": ' + year + '},'

            # Skip header and handle each entry.
            entries_string = ""
            next(reader)
            print(race_name)
            for row in reader:
                # Generate a new JSON string for this entry.
                new_entry_string = _get_entry_string(row)

                if len(entries_string) > 0:
                    entries_string += ', '
                entries_string += new_entry_string

                # Meta stuff for the user.
                entry_count += 1
                _print_debug(repr(input_path) + ": " + str(entry_count))

            race_json = json.loads('{' + meta_string + entries_string + '}')
            with open(output_path, "w") as out_file:
                json.dump(race_json, out_file, sort_keys=True, indent=4)

    except _Error as e:
        return -1

    return 0

def _clean_string(string):
    """Escapes any quotes in string."""
    return string.replace('\"', '\\\"')

def _format_number(number):
    """Repetitive JSON formatting for numbers."""
    if number == None or number == "":
        return 'null'
    else:
        return number

def _format_string(string):
    """Repetitive JSON formatting for strings."""
    if string == None or string == "":
        return 'null'
    else:
        return '"' + _clean_string(string) + '"'

def _get_entry_string(row):
    """Returns a JSON string representation of the entry."""
    entry_string = '"' + str(row[0])                                        \
                   + '": {"Number": '        + _format_number(str(row[1]))  \
                   + ', "Team Name": '       + _format_string(str(row[2]))  \
                   + ', "Class": '           + _format_string(str(row[3]))  \
                   + ', "Year": '            + _format_number(str(row[4]))  \
                   + ', "Make": '            + _format_string(str(row[5]))  \
                   + ', "Model": '           + _format_string(str(row[6]))  \
                   + ', "Laps": '            + _format_number(str(row[7]))  \
                   + ', "Best Time": '       + _format_string(str(row[8]))  \
                   + ', "BS Penalty Laps": ' + _format_number(str(row[9]))  \
                   + ', "Black Flag Laps": ' + _format_number(str(row[10])) \
                   + '}'
    return entry_string

def _csv_path(filename):
    return os.path.normpath(_csv_dir + "/" + filename + ".csv")

def _json_path(filename):
    return os.path.normpath(_json_dir + "/" + filename + ".json")

def _print_debug(err):
    if _debug:
      print(err)

def _main(args):
    global _debug
    global _csv_dir
    global _json_dir
    global _root_dir

    counter = 0
    _debug = False

    if args["-d"]:
        _debug = True

    _root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/..")
    _csv_dir  = os.path.normpath(_root_dir + "/csv")
    _json_dir = os.path.normpath(_root_dir + "/json")

    # For each CSV, read and convert it to JSON.
    for file in os.listdir(_csv_dir):
        if file.endswith(".csv"):
            filename = os.path.splitext(file)[0]

            _print_debug("Processing: " + filename)
            result = _convert(_csv_path(filename), _json_path(filename))

            # Handle any possible errors; otherwise, chalk up another success!
            if result == 0:
                counter += 1
            elif result == 1:
                raise _InputFileError(filename)
            elif result == 2:
                raise _OutputFileError(filename)
            else:
                raise _HooptieError(filename, result)

    if counter > 0:
      print("\nProcessed " + str(counter) + " records.")
    else:
      print("Did not process any records.")

    return

if __name__ == "__main__":
    _main(docopt(__doc__, help=True, version=__version__))
    exit(0)
