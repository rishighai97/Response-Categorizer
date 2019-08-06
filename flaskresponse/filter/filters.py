import pickle
import os
from flask import current_app
from operator import itemgetter


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

'''
0 - question
1 - accepted answer
2 - answers
 que, accepted_answer, [ans_id, answer_user, answer, score, [comm_user, comm, score, pol]]
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
		# que, accepted_answer, [ans_id, answer_user, answer, score, [comm_user, comm, score, pol]]
		temp_asc = []
		temp_desc = []
		temp_asc.append(i)
		temp_asc.append(results[5][i])
		temp_asc.append(results[1][i])
		temp_asc.append(results[9][i])
		temp_desc.append(i)
		temp_desc.append(results[5][i])
		temp_desc.append(results[1][i])
		temp_desc.append(results[9][i])
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
				#print(results[6])
				temp.append(results[6][i][k])
				temp.append(results[2][i][k])
				temp.append(results[8][i][k])
				temp.append(results[7][i][k])

				comments.append(temp)
		comments_asc = sorted(comments, key = itemgetter(2))
		comments_desc = sorted(comments, key = itemgetter(2), reverse = True)	
		temp_asc.append(comments_asc)
		temp_desc.append(comments_desc)
		answers_asc.append(temp_asc)
		answers_desc.append(temp_desc)		
	answers_asc = sorted(answers_asc,key = itemgetter(3))
	answers_desc = sorted(answers_desc,key = itemgetter(3), reverse = True)
	final_asc.append(answers_asc)
	final_desc.append(answers_desc)
	final = []
	final.append(final_asc)
	final.append(final_desc)
	path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')
	with open(path, "wb") as fp:   
		pickle.dump(final, fp)
