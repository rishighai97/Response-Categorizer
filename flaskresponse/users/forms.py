from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskresponse.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
							validators=[DataRequired(),Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
									validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')


	# If form is validated. We need to check if the username and email are not repeated as both are unique fields in the model User (models.py) Thus, we use custom validaton by raising ValidationError
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('The username is taken. Please choose a different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('The email id is taken. Please choose a different email id')



class LoginForm(FlaskForm):
	email = StringField('Email',
							validators=[DataRequired(),Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')



class UpdateAccountForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
							validators=[DataRequired(),Email()])
	picture = FileField('Update Profile picture', validators=[FileAllowed(['png','jpg','jpeg'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('The username is taken. Please choose a different username')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('The email id is taken. Please choose a different email id')

