#!flask/bin/python

# Name:         run.py
# Authors:      Matthew Sheridan
# Date:         22 July 2017
# Revision:     22 July 2017
# Copyright:    Matthew Sheridan 2017
# Licence:      Beer-Ware License Rev. 42

print(' * Flask messages.')
print(' + sweet-db messages.')
print('Starting sweet-db . . .')

from app import app
app.run(debug=True,port=5543)
