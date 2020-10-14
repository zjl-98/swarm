"""
 Created by zjl on 2020/9/26 21:14
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp

__author__ = 'zjl'


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    type = IntegerField(validators=[NumberRange(min=0, max=3)])


# class MoviePageForm(Form):
#     page = IntegerField(validators=[NumberRange(min=1)])