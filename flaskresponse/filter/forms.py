from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskresponse.models import User

class FilterForm(FlaskForm):
	url = StringField('URL', 
							validators=[Length(min=0, max=2000)])
	submit_url = SubmitField('Submit URL')

	submit_filter = SubmitField('Filter')

class SortingForm(FlaskForm):
	htl = SubmitField('High To Low')
	lth = SubmitField('Low To High')
	minimum = StringField('Start',default = 0)
	maximum = StringField('End',default = 100)


