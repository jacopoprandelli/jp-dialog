from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length


class BaseForm(FlaskForm):
    number = IntegerField('Number', validators=[InputRequired()])
    name = StringField('Name', validators=[Length(min=1, max=50),DataRequired()])
    submit = SubmitField('Submit')