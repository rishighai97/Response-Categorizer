import pickle
import os
from flask import current_app


def retrieve_level1_data():
	question_path = os.path.join(current_app.root_path, 'static/pickles','question.pickle')
	with open(question_path, "rb") as fp:
		question = pickle.load(fp)
	answers_path = os.path.join(current_app.root_path, 'static/pickles','answers.pickle')
	with open(answers_path, "rb") as fp:
		answers = pickle.load(fp)
	comments_path = os.path.join(current_app.root_path, 'static/pickles','comments.pickle')
	with open(comments_path, "rb") as fp:
		comments = pickle.load(fp)
	accepted_answer_path = os.path.join(current_app.root_path, 'static/pickles','accepted_answer.pickle')
	with open(accepted_answer_path, "rb") as fp:
		accepted_answer = pickle.load(fp)
	accepted_comments_path = os.path.join(current_app.root_path, 'static/pickles','accepted_comments.pickle')
	with open(accepted_comments_path, "rb") as fp:
		accepted_comments = pickle.load(fp)
	comments_polarity_path = os.path.join(current_app.root_path, 'static/pickles','comments_polarity.pickle')
	with open(comments_polarity_path, "rb") as fp:
		comments_polarity = pickle.load(fp)	
	return question,answers,comments,accepted_answer,accepted_comments, comments_polarity


def retrieve_level2_data():
	comments_score_path = os.path.join(current_app.root_path, 'static/pickles','comments_score.pickle')
	with open(comments_score_path, "rb") as fp:
		comments_score = pickle.load(fp)
	answers_score_path = os.path.join(current_app.root_path, 'static/pickles','answers_score.pickle')
	with open(answers_score_path, "rb") as fp:
		answers_score = pickle.load(fp)
	return comments_score,answers_score