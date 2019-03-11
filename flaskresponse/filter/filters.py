import pickle
import os
from flask import current_app
from operator import itemgetter

'''
0 - question
1 - accepted answer
2 - answers
 que, accepted_answer, [ans_id, answer, score, [comm, score, pol]]
'''

def filter_dump(results):
	final_asc = []
	final_asc.append(results[0])
	final_asc.append(results[3])
	final_desc = []
	final_desc.append(results[0])
	final_desc.append(results[3])
	answers_asc = []
	answers_desc = []
	for i in range(0,len(results[1])):
		# que, accepted_answer, [ans_id, answer, score, [comm, score, pol]]
		temp_asc = []
		temp_desc = []
		temp_asc.append(i)
		temp_asc.append(results[1][i])
		temp_asc.append(results[7][i])
		temp_desc.append(i)
		temp_desc.append(results[1][i])
		temp_desc.append(results[7][i])
		comments = []

		comm = results[2][i]
		temp = []
		if comm == 'none':
			temp.append('none')
			temp.append(-1)
			temp.append(-1)
		else:
			for k in range(0,len(comm)):
				temp = []
				temp.append(results[2][i][k])
				temp.append(results[6][i][k])
				temp.append(results[5][i][k])
				comments.append(temp)
		comments_asc = sorted(comments, key = itemgetter(1))
		comments_desc = sorted(comments, key = itemgetter(1), reverse = True)	
		temp_asc.append(comments_asc)
		temp_desc.append(comments_desc)
		answers_asc.append(temp_asc)
		answers_desc.append(temp_desc)		
	answers_asc = sorted(answers_asc,key = itemgetter(2))
	answers_desc = sorted(answers_desc,key = itemgetter(2), reverse = True)
	final_asc.append(answers_asc)
	final_desc.append(answers_desc)
	final = []
	final.append(final_asc)
	final.append(final_desc)
	path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')
	with open(path, "wb") as fp:   
		pickle.dump(final, fp)
