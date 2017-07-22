# Name:         sweetutils.py
# Authors:      Matthew Sheridan
# Date:         21 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

def _print(msg):
    print(str(__file__) + ':\n * ' + msg)

def _print_debug(msg):
    _print(msg)

def _print_warn(msg):
    print(str(__file__) + ':\n * WARNING: ' + str(msg))
