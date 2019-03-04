
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
#import gensim.models.keyedvectors as word2vec
lemmatizer = WordNetLemmatizer()
library_path = os.path.join(current_app.root_path, 'static/libraries','GoogleNews-vectors-negative300.bin')
model = gensim.models.KeyedVectors.load_word2vec_format(library_path, binary=True,limit=500000)  




comments_path = os.path.join(current_app.root_path, 'static/pickles','comments.pickle')
with open(comments_path, "rb") as fp:
        comments = pickle.load(fp)
 
answers_path = os.path.join(current_app.root_path, 'static/pickles','answers.pickle')
with open(answers_path, "rb") as fp:
        answers = pickle.load(fp)
    
accepted_answer_path = os.path.join(current_app.root_path, 'static/pickles','accepted_answer.pickle')
with open(accepted_answer_path, "rb") as fp:
        accepted_answer = pickle.load(fp)     
    



#sentence = ''.join(e for e in sentence if e.isalnum()) # only alphanumerals

minimum = float('inf')
maximum = float('-inf')

comments_score = []
for comm in comments:
	if comm == 'none':
		comments_score.append('none')
	else:
		score = []
		for c in comm:
			current_words = word_tokenize(c)
			current_words = [lemmatizer.lemmatize(i).lower() for i in current_words]
			val = model.wmdistance(current_words, accepted_answer)
			if val<=minimum:
				minimum = val
			if val>=maximum:
				maximum = val
			score.append(val)
		comments_score.append(score)

answers_score = []
for ans in answers:
	current_words = word_tokenize(ans)
	current_words = [lemmatizer.lemmatize(i).lower() for i in current_words]
	val = model.wmdistance(current_words, accepted_answer)
	if val<=minimum:
		minimum = val
	if val>=maximum:
		maximum = val				
	answers_score.append(val)


final_answers_score = []
for score in answers_score:
	val = (score-minimum)/(maximum-minimum)
	val = 1 - val
	val = Decimal(val)
	val = val.quantize(Decimal('0.0001'))
	final_answers_score.append(val)

final_comments_score = []
for c in comments_score:
	if c == 'none':
		final_comments_score.append('none')
	else:
		temp = []
		for score in c:
			val = (score-minimum)/(maximum-minimum)
			val = 1 - val
			val = Decimal(val)
			val = val.quantize(Decimal('0.0001'))
			temp.append(val)
		final_comments_score.append(temp)
		

	
comments_score_path = os.path.join(current_app.root_path, 'static/pickles','comments_score.pickle')			
with open(comments_score_path, "wb") as fp:
        pickle.dump(final_comments_score,fp) 
        

answers_score_path = os.path.join(current_app.root_path, 'static/pickles','answers_score.pickle')		
with open(answers_score_path, "wb") as fp:
        pickle.dump(final_answers_score,fp) 
        





'''
distance = model.wmdistance(sentence_obama, sentence_president)
print('distance = %.4f' % distance)
'''
