import pickle
import os
from flask import current_app
import matplotlib.pyplot as plt



def dump_data(question,answers,comments,accepted_answer,accepted_comments,answers_user, comments_user):
	data = []
	data.append(question)
	data.append(answers)
	data.append(comments)
	data.append(accepted_answer)
	data.append(accepted_comments)
	data.append(answers_user)
	data.append(comments_user)
	path = os.path.join(current_app.root_path, 'static/pickles','data.pickle')
	with open(path, "wb") as fp:   
		pickle.dump(data, fp)


def retrieve_data():
	path = os.path.join(current_app.root_path, 'static/pickles','data.pickle')
	with open(path, "rb") as fp:
		data = pickle.load(fp)
	return data


def retrieve_results():
	path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')
	with open(path, "rb") as fp:
		results = pickle.load(fp)
	return results
	
def clear_results_file():
	path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')
	with open(path, "wb") as fp:   
		pickle.dump([], fp)


'''
0 - question
1 - answers
2 - comments
3 - accepted_answer
4 - accepted_comments
5 - answers_user
6 - comments_user
7 - comments_polarity
8 - comments_score
9 - answers_score
'''