from flask_wtf import Form
from wtforms import StringField, BooleanField

class SearchForm(Form):
    event = StringField('event')
    team  = StringField('team')
    make  = StringField('make')
    model = StringField('model')
