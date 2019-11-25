from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RoleEntry(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    manager = StringField('Hiring Manager', validators=[DataRequired()])
    submit = SubmitField('Create Role')