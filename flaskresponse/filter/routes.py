from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskresponse.filter.forms import FilterForm 
import requests
from flask_login import login_user, current_user, logout_user, login_required 
from flaskresponse.filter.utils import retrieve_level1_data, retrieve_level2_data
from flaskresponse.filter.scrape import cleanhtml, get_question_answers_comments, print_answers_comments, get_accepted_answer_comments,dump_data,retrieve_data
import re
from bs4 import BeautifulSoup
import pickle
import pandas as pd

filter_blueprint = Blueprint('filter_blueprint', __name__)

@filter_blueprint.route("/filter", methods=['GET','POST'])
@login_required
def filter():
	form = FilterForm()
	if form.validate_on_submit():
		if form.submit.data:
			page = requests.get(form.url.data)
			soup = BeautifulSoup(page.content, 'html.parser')
			question, answers, comments = get_question_answers_comments(soup)
			accepted_answer, accepted_comments = get_accepted_answer_comments(soup)
			dump_data(question,answers,comments,accepted_answer,accepted_comments)
			flash('Question, answers and comments from the specified URL are successfully extracted','success')
			return render_template('before_filter_display.html', title='Before', question = question, answers = answers,comments = comments, accepted_answer = accepted_answer, accepted_comments = accepted_comments)
		if form.submit_level1.data:
			question,answers,comments,accepted_answer,accepted_comments = retrieve_data()
			#filter_blueprintlevel1()
			from flaskresponse.filter import level1
			question,answers,comments,accepted_answer,accepted_comments, comments_polarity = retrieve_level1_data()
			return render_template('level1_display.html',title='Level1',question = question, answers = answers,comments = comments, accepted_answer = accepted_answer, accepted_comments = accepted_comments, comments_polarity = comments_polarity)
		if form.submit_level2.data:
			from flaskresponse.filter import level2
			question,answers,comments,accepted_answer,accepted_comments, comments_polarity = retrieve_level1_data()
			comments_score, answers_score = retrieve_level2_data()
			return render_template('level2_display.html',title='Level2',question = question, answers = answers,comments = comments, accepted_answer = accepted_answer, accepted_comments = accepted_comments, comments_polarity = comments_polarity, comments_score = comments_score, answers_score = answers_score)
	return render_template('url.html',title='Upload',form=form,legend ='Enter URL')


@filter_blueprint.route("/before_filter_display")
@login_required
def before_filter_display():
	question,answers,comments,accepted_answer,accepted_comments = retrieve_data()
	return render_template('before_filter_display.html', title='Before', question = question, answers = answers,comments = comments, accepted_answer = accepted_answer, accepted_comments = accepted_comments)

@filter_blueprint.route("/level1_display")
@login_required
def level1_display():
	question,answers,comments,accepted_answer,accepted_comments, comments_polarity = retrieve_level1_data()
	return render_template('level1_display.html',title='Level1',question = question, answers = answers,comments = comments, accepted_answer = accepted_answer, accepted_comments = accepted_comments, comments_polarity = comments_polarity)


@filter_blueprint.route("/level2_display")
@login_required
def level2_display():
	question,answers,comments,accepted_answer,accepted_comments, comments_polarity = retrieve_level1_data()
	comments_score, answers_score = retrieve_level2_data()
	return render_template('level2_display.html',title='Level2',question = question, answers = answers,comments = comments, accepted_answer = accepted_answer, accepted_comments = accepted_comments, comments_polarity = comments_polarity, comments_score = comments_score, answers_score = answers_score)

