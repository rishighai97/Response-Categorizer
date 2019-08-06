from flask import render_template, Blueprint, url_for

main = Blueprint('main', __name__)

@main.route("/home") # routes for home page
def home():
	img = url_for('static',filename='images/home_bg.jpg')
	return render_template('home.html',img=img) # render template is used to display the page to be displayed when the route is called. posts is passed and displayed on home page using Jinja templating
    

@main.route("/about")
def about():
    return render_template('about.html',title='about') # title is set as About. Wherever know title is passed, default title is used
