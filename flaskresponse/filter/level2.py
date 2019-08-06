
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
	min_wm = 0
	max_wm = 4

	min_ln = 0
	max_ln = 1
	ln_ans = len(word_tokenize(accepted_answer))

	accepted = word_tokenize(accepted_answer)
	accepted = [lemmatizer.lemmatize(i).lower() for i in accepted]

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
				val_wm = model.wmdistance(current_words, accepted)
				if val_wm>4:
					val_wm = 0
				else:
					val_wm = (val_wm - min_wm)/(max_wm-min_wm)
					val_wm = 1 - val_wm	
				score_wm.append(val_wm)

				val_ln=len(current_words)/ln_ans
				
				if val_ln<=0.08:
					val_ln = 0
				elif val_ln>=1:
					val_ln = 1
				else:
					val_ln = (val_ln - min_ln)/(max_ln - min_ln)


				score_ln.append(val_ln)
			comments_score.append(score_wm)
			comments_length.append(score_ln)


	answers_score = []
	answers_length = []
	for ans in answers:
		current_words = word_tokenize(ans)
		current_words = [lemmatizer.lemmatize(i).lower() for i in current_words]
		val_wm = model.wmdistance(current_words, accepted)
		if val_wm>4:
			val_wm = 0
		else:
			val_wm = (val_wm - min_wm)/(max_wm-min_wm)
			val_wm = 1 - val_wm	
		
		val_ln = len(current_words)/ln_ans
		
		
		if val_ln<=0.08:
			val_ln = 0
		elif val_ln>=1:
			val_ln = 1
		else:
			val_ln = (val_ln - min_ln)/(max_ln - min_ln)
		
		answers_score.append(val_wm)
		answers_length.append(val_ln)

	

	return comments_score,comments_length,answers_score,answers_length

def final_score(comments_wm,comments_ln,answers_wm,answers_ln,comments_polarity):
	answers_score = []
	wm = 0
	ln = 0
	for i in range(0,len(answers_wm)):

		if answers_ln[i] <= 0.2:
			ln = 0.8
			wm = 0.2
		elif answers_ln[i] > 0.2 and answers_ln[i] <= 0.5:
			ln = 0.6
			wm = 0.4
		elif answers_ln[i] > 0.5 and answers_ln[i] <= 0.8:
			ln = 0.4
			wm = 0.6
		elif answers_ln[i] > 0.8 and answers_ln[i] <= 1:
			ln = 0.3
			wm = 0.7

		answers_val = answers_wm[i]*wm+answers_ln[i]*ln
		#answers_val = answers_ln[i]
		answers_val = answers_val * 100
		answers_val = round(answers_val,2)
		answers_score.append(answers_val)
	wm = 0
	ln = 0
	pol = 0
	comments_score = []
	for i in range(len(comments_wm)):
		if comments_wm[i] == 'none':
			comments_score.append('none')
		else:
			temp_score = []
			for j in range(0,len(comments_wm[i])):

				if comments_ln[i][j] <= 0.3:
					ln = 0.85
					wm = 0.05
				elif comments_ln[i][j] > 0.3 and comments_ln[i][j] <= 0.5:
					ln = 0.65
					wm = 0.25
				elif comments_ln[i][j] > 0.5 and comments_ln[i][j] <= 0.8:
					ln = 0.25
					wm = 0.65
				elif comments_ln[i][j] > 0.8 and comments_ln[i][j] <= 1:
					ln = 0.2
					wm = 0.7

				if answers_score[i]>=50:
					if comments_polarity[i][j]==1:
						pol = 0.1
					else:
						pol = 0
				else:
					if comments_polarity[i][j]==0:
						pol = 0.1
					else:
						pol = 0
				comments_val = comments_ln[i][j]*ln+ comments_wm[i][j]*wm + pol
				#comments_val = comments_ln[i][j]
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
