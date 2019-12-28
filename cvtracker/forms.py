from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from cvtracker.models import CV, Hirer, Role, Source, Cvstatus, Rolestatus, Statuschange


class MgrEntry(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleEntry(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    date_opened = DateField('Date Opened', format='%Y-%m-%d')
    manager = SelectField(u'Hiring Manager', choices=[], coerce=int)
    rolestatus = SelectField(u'RoleStatus', choices=[], coerce=int)
    submit = SubmitField('Submit')

class CVEntry(FlaskForm):
    reference = StringField('Reference', validators=[DataRequired()])
    cvnotes = TextAreaField('Notes')
    date_entered = DateField('Date Entered', format='%Y-%m-%d')
    role = SelectField(u'Role', choices=[], coerce=int)
    source = SelectField(u'Source', choices=[], coerce=int)
    cvstatus = SelectField(u'CVStatus', choices=[], coerce=int)
    submit = SubmitField('Submit')

class SourceEntry(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CVStatus(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleStatus(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')