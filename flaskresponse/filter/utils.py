import pickle
import os
from flask import current_app

def dump_data(question,answers,comments,accepted_answer,accepted_comments):
	data = []
	data.append(question)
	data.append(answers)
	data.append(comments)
	data.append(accepted_answer)
	data.append(accepted_comments)
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
	



'''
0 - question
1 - answers
2 - comments
3 - accepted_answer
4 - accepted_comments
5 - comments_polarity
6 - comments_score
7 - answers_score
'''