from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from cvtracker.models import CV, Hirer, Role


class MgrEntry(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleEntry(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    date_opened = DateField('Date Opened', format='%Y-%m-%d')
    #manager = SelectField(u'Hiring Manager', choices=[(g.id, g.name) for g in Hirer.query.all()])
    manager = StringField('Manager', validators=[DataRequired()])
    submit = SubmitField('Submit')