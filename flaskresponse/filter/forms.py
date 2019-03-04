from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskresponse.models import User

class FilterForm(FlaskForm):
	url = StringField('URL', 
							validators=[Length(min=0, max=2000)])
	submit = SubmitField('Submit URL')

	submit_level1 = SubmitField('Level 1 filter')
	submit_level2 = SubmitField('Level 2 filter')

