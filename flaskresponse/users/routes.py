from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskresponse import db, bcrypt 
from flaskresponse.models import User
from flaskresponse.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required 
from flaskresponse.users.utils import save_picture
import requests

users = Blueprint('users', __name__)

@users.route("/register",methods=['GET','POST'])
def register(): 
	if current_user.is_authenticated: # is user is authenticated, redirect him to home
		return redirect(url_for('main.home'))
	form = RegistrationForm() # An object of the Registration form is created. 
	if form.validate_on_submit(): # If the user hits the submit button, the form is validated based on the default and custom validators in the forms.py Registration class. If there are no errors, the code block below is executed
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
		user = User(username=form.username.data, email=form.email.data, password=hashed_password) # User info recieved from form is stored in User model from models.py
		db.session.add(user) # We use add method to add the user object filled with data into user(first letter lowercase of class User) table in sql alchemy db 
		db.session.commit() # We commit the changes to the database
		flash('Your account has been created! You are now able to log in','success') # flash message is displayed on login page and class is set as success to get a green message, which is done in layout.html
		return redirect(url_for('users.login')) # User is refirected to login page so that now they can login to the system
	return render_template('register.html',title='Register',form=form) # The form object is passed to the view and the components are displayed using jinja templating. If any errors are there, they are also displayed in the view (register.html)

@users.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first() # We check if the user with specified email is present 
		if user and bcrypt.check_password_hash(user.password, form.password.data): # If the user exists and the password matches with the password in db, user is authenticated
			login_user(user, remember=form.remember.data) # We accept yes/no from rememeber me boolean field
			next_page = request.args.get('next') # next arguement from the url is used to redirect the user to desired page if he directly tried to access a page via url 
			return redirect(next_page) if next_page else redirect(url_for('filter_blueprint.filter')) # We redirect the user to home page after successful login
		else:
			flash('Login Unsuccessful. Please check username and password','danger') # If user is not authenticated, we display a flash message with class='danger' which is set in the layout.html
	return render_template('login.html',title='Login',form=form) 

@users.route("/logout")
def logout():
	logout_user() # logs out the user from login_manager system
	return redirect(url_for('main.home')) # User is redirected to home after logout


@users.route("/account",methods=['GET','POST']) 
@login_required # This page is accessible if the user is logged in
def account():
	form = UpdateAccountForm() # Instance of form
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data) # if new image is uploaded, it is stored in the database
			current_user.image_file = picture_file # the image file uploaded is direclty stored in current_user and the data is automatically synched with sql database after commit
		current_user.username = form.username.data # new username is stored
		current_user.email = form.email.data # new email is stored
		db.session.commit() # commit updates the values changed in current_user in the database
		flash('Your account has been updated','success') # A message is flashed suggesting that updates where successful
		return redirect(url_for('users.account')) # post get redirect (avoid data will be resubmitted message)
	elif request.method == 'GET': # (Pre populating the fields)If the page is accessed in general, the original username and email are displayed.
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static',filename='profile_pics/'+current_user.image_file) # image file is also passed to the view (account.html)
	return render_template('account.html',title='Account',image_file=image_file, form=form) # (Populating the form in view)render the view and display error messages, if any

