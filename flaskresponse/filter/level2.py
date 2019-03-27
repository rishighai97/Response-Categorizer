
# Import and download stopwords from NLTK.
from nltk.corpus import stopwords
import os
import gensim
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pickle
import sys
from decimal import Decimal
from flask import current_app
from flaskresponse.filter.filters import filter_dump
#import gensim.models.keyedvectors as word2vec
lemmatizer = WordNetLemmatizer()
library_path = os.path.join(current_app.root_path, 'static/libraries','GoogleNews-vectors-negative300.bin')
model = gensim.models.KeyedVectors.load_word2vec_format(library_path, binary=True,limit=500000)  

def retrieve():
	path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')
	with open(path, "rb") as fp:
		results = pickle.load(fp)
	return results
     
def word_movers_score(comments,answers,accepted_answer):
	min_wm_ans = float('inf')
	max_wm_ans = float('-inf')
	min_ln_ans = float('inf')
	max_ln_ans = float('-inf')

	min_wm_comm = float('inf')
	max_wm_comm = float('-inf')
	min_ln_comm = float('inf')
	max_ln_comm = float('-inf')

	comments_score = []
	comments_length = []
	for comm in comments:
		if comm == 'none':
			comments_score.append('none')
			comments_length.append('none')
		else:
			score_wm = []
			score_ln = []
			for c in comm:
				current_words = word_tokenize(c)
				current_words = [lemmatizer.lemmatize(i).lower() for i in current_words]
				acc = word_tokenize(accepted_answer)
				acc = [lemmatizer.lemmatize(i).lower() for i in acc]
				val_wm = model.wmdistance(current_words, acc)
				if val_wm<=min_wm_comm:
					min_wm_comm = val_wm
				if val_wm>max_wm_comm:
					max_wm_comm = val_wm
				score_wm.append(val_wm)
				val_ln=len(current_words)/len(word_tokenize(accepted_answer))
				if val_ln<=min_ln_comm:
					min_ln_comm = val_ln
				if val_ln>max_ln_comm:
					max_ln_comm = val_ln
				score_ln.append(val_ln)
			comments_score.append(score_wm)
			comments_length.append(score_ln)


	answers_score = []
	answers_length = []
	for ans in answers:
		current_words = word_tokenize(ans)
		current_words = [lemmatizer.lemmatize(i).lower() for i in current_words]
		acc = word_tokenize(accepted_answer)
		acc = [lemmatizer.lemmatize(i).lower() for i in acc]
		val_wm = model.wmdistance(current_words, accepted_answer)
		if val_wm<=min_wm_ans:
			min_wm_ans = val_wm
		if val_wm>max_wm_ans:
			max_wm_ans = val_wm	
		val_ln = len(current_words)/len(word_tokenize(accepted_answer))
		if val_ln<=min_ln_ans:
			min_ln_ans = val_ln
		if val_ln>max_ln_ans:
			max_ln_ans = val_ln				
		answers_score.append(val_wm)
		answers_length.append(val_ln)

	final_answers_score_wm = []
	final_answers_score_ln = []
	for i in range(0,len(answers_score)):
		val_wm = (answers_score[i]-min_wm_ans)/(max_wm_ans-min_wm_ans)
		val_wm = 1 - val_wm
		final_answers_score_wm.append(val_wm)

		val_ln = (answers_length[i]-min_ln_ans)/(max_ln_ans-min_ln_ans)
		'''val_ln = Decimal(val_ln)
		val_ln = val_ln.quantize(Decimal('0.0001'))'''
		final_answers_score_ln.append(val_ln)


	final_comments_score_wm = []
	final_comments_score_ln = []
	for i  in range(len(comments_score)):
		if comments_score[i] == 'none':
			final_comments_score_wm.append('none')
			final_comments_score_ln.append('none')
		else:
			temp_wm = []
			temp_ln = []
			for j in range(0,len(comments_score[i])):
				val_wm = (comments_score[i][j]-min_wm_comm)/(max_wm_comm-min_wm_comm)
				val_wm = 1 - val_wm
				temp_wm.append(val_wm)

				val_ln = (comments_length[i][j]-min_ln_comm)/(max_ln_comm-min_ln_comm)
				temp_ln.append(val_ln)
			final_comments_score_wm.append(temp_wm)
			final_comments_score_ln.append(temp_ln)
			#final_score()

	return final_comments_score_wm,final_comments_score_ln,final_answers_score_wm,final_answers_score_ln

def final_score(comments_wm,comments_ln,answers_wm,answers_ln,comments_polarity):
	answers_score = []
	for i in range(0,len(answers_wm)):
		answers_val = answers_wm[i]*0.6+answers_ln[i]*0.4
		answers_val = answers_val * 100
		answers_val = round(answers_val,2)
		answers_score.append(answers_val)

	comments_score = []
	for i in range(len(comments_wm)):
		if comments_wm[i] == 'none':
			comments_score.append('none')
		else:
			temp_score = []
			for j in range(0,len(comments_wm[i])):
				if answers_score[i]>=50:
					if comments_polarity[i][j]==1:
						pol = 0.2
					else:
						pol = 0
				else:
					if comments_polarity[i][j]==0:
						pol = 0.2
					else:
						pol = 0
				comments_val = comments_ln[i][j]*0.3 + comments_wm[i][j]*0.5 + pol
				comments_val = comments_val*100
				comments_val = round(comments_val,2)
				temp_score.append(comments_val)
			comments_score.append(temp_score)
	return comments_score, answers_score








def filter_level2():
	results = retrieve()
	comments = results[2]
	answers = results[1]
	accepted_answer = results[3]
	comments_polarity = results[7]

	comments_wm,comments_ln,answers_wm,answers_ln = word_movers_score(comments,answers,accepted_answer)
	comments_score,answers_score = final_score(comments_wm,comments_ln,answers_wm,answers_ln,comments_polarity)
	print('In Level 2')


	results.append(comments_score)
	results.append(answers_score)
	'''
	path = os.path.join(current_app.root_path, 'static/pickles','results.pickle')			
	with open(path, "wb") as fp:
        pickle.dump(results,fp) 
	'''
	filter_dump(results)
        


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
distance = model.wmdistance(sentence_obama, sentence_president)
print('distance = %.4f' % distance)
'''
