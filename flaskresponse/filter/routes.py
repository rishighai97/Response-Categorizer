from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskresponse.filter.forms import FilterForm, SortingForm
import requests
from flask_login import login_user, current_user, logout_user, login_required 
from flaskresponse.filter.utils import dump_data, retrieve_data, retrieve_results, clear_results_file
from flaskresponse.filter.scrape import cleanhtml, get_question_answers_comments, print_answers_comments, get_accepted_answer_comments
import re
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import tensorflow as tf


filter_blueprint = Blueprint('filter_blueprint', __name__)

@filter_blueprint.route("/report")
@login_required
def report():
	data = retrieve_data()
	results = retrieve_results()
	results_asc = results[0]
	results_desc = results[1]
	return render_template('report.html', title='Report', result=results_desc)


@filter_blueprint.route("/filter", methods=['GET','POST'])
@login_required
def filter():
	form = FilterForm()
	if form.validate_on_submit():
		if form.submit_url.data:
			page = requests.get(form.url.data)
			soup = BeautifulSoup(page.content, 'html.parser')
			question, answers, comments, answers_user, comments_user = get_question_answers_comments(soup)
			accepted_answer, accepted_comments = get_accepted_answer_comments(soup)
			dump_data(question,answers,comments,accepted_answer,accepted_comments, answers_user, comments_user)
			flash('Question, answers and comments from the specified URL are successfully extracted','success')
			data = retrieve_data()
			return render_template('before_filter_display.html', title='Data', question = data[0], answers = data[1],comments = data[2], accepted_answer = data[3], accepted_comments = data[4], answers_user = data[5], comments_user = data[6])
		if form.submit_filter.data:
			print('Start')
			import flaskresponse.filter.level1 as f1
			f1.filter_level1()
			print('After level 1')
			import flaskresponse.filter.level2 as f2
			f2.filter_level2()
			print('After level 2')
			results = retrieve_results()
			results_asc = results[0]
			results_desc = results[1]
			form = SortingForm()
			return render_template('filter_results.html', form=form, title='Results',result = results_desc, minimum = 0, maximum = 100)
	return render_template('url.html',title='Upload',form=form,legend ='Enter URL')


@filter_blueprint.route("/before_filter_display")
@login_required
def before_filter_display():
	data = retrieve_data()
	return render_template('before_filter_display.html', title='Data', question = data[0], answers = data[1],comments = data[2], accepted_answer = data[3], accepted_comments = data[4], answers_user = data[5], comments_user = data[6])


@filter_blueprint.route("/filter_results",methods=['GET', 'POST'])
@login_required
def filter_results():
	form = SortingForm()
	results = retrieve_results()
	results_asc = results[0]
	results_desc = results[1]
	if form.validate_on_submit():
		minimum = float(form.minimum.data)
		maximum = float(form.maximum.data)
		if form.htl.data:
			return render_template('filter_results.html', form=form, title='Results', result=results_desc, minimum = minimum, maximum = maximum)
		if form.lth.data:
			return render_template('filter_results.html', form=form, title='Results', result=results_asc, minimum = minimum, maximum = maximum)	
	return render_template('filter_results.html', form=form, title='Results', result=results_desc, minimum = 0, maximum = 100)
