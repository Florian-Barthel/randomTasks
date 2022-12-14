from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import InputRequired, NumberRange


class CreateTaskForm(FlaskForm):
    name_create = TextField('Task Name', validators=[InputRequired()])
    energy_create = IntegerRangeField('Energy', default=5, validators=[NumberRange(min=0, max=10)])
    time_create = IntegerRangeField('Time', default=5, validators=[NumberRange(min=0, max=10)])
    priority_create = IntegerRangeField('Priority', default=5, validators=[NumberRange(min=0, max=10)])
    submit_create = SubmitField('Create')


class BestMatchingTasks(FlaskForm):
    energy = IntegerRangeField('Energy', default=5, validators=[NumberRange(min=0, max=10)])
    time = IntegerRangeField('Time', default=5, validators=[NumberRange(min=0, max=10)])
    submit_match = SubmitField('Calculate')
