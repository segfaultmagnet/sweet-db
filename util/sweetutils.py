# Name:         sweetutils.py
# Authors:      Matthew Sheridan
# Date:         21 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

import os

def _print(file, msg):
    print(str(os.path.basename(file)) + ':\n + ' + msg)

def _print_debug(file, msg):
    _print(file, msg)

def _print_raw(file, msg):
    msg = '\n' + msg
    msg = msg.replace('\n', '\n  ')
    print(str(os.path.basename(file)) + ':\n' + msg + '\n')

def _print_warn(file, msg):
    print(str(os.path.basename(file)) + ':\n + WARNING: ' + str(msg))
