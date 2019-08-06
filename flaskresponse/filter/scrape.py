# script to scrape questions, answers and comments from stack overflow and stack exchange

# imports
import requests
import re
from bs4 import BeautifulSoup
import pickle
import os
from flask import current_app





def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
'''
for ans in soup.find_all(class_='answer'):
	print()
	if ans.find_all(class_='comment-user'):
		for c in ans.find_all(class_='comment-user'):
			print(c.get_text())
		print('\n')
'''

def get_question_answers_comments(soup):
	question = cleanhtml(soup.find(class_= 'question-hyperlink').get_text())
	answers = []
	answers_user = []
	comments = []
	comments_user = []
	for ans in soup.find_all(class_ = 'answer'):
		if ans.find(class_='js-accepted-answer-indicator grid--item fc-green-500 ta-center p4'):
			continue
		text = ans.find(class_='post-text').get_text()
		answers.append(text)
		if ans.find(class_='user-details').findChild():
			answers_user.append(cleanhtml(ans.find(class_='user-details').findChild().get_text()))
		else:
			answers_user.append(cleanhtml(ans.find(class_='user-details').get_text()))
		if ans.find_all(class_='comment-copy'):
			temp = []
			temp_user = []
			for c in ans.find_all(class_='comment-copy'):
				text = cleanhtml(c.get_text())
				temp.append(text)
			for c in ans.find_all(class_='comment-user'):
				temp_user.append(c.get_text())
			comments.append(temp)
			comments_user.append(temp_user)
		else:
			comments.append('none') # 'none' if no comments
			comments_user.append('none')
	return question, answers, comments, answers_user, comments_user

def print_answers_comments(answers,comments):
	for i in range(len(answers)):
		print("\n\n\n\nAnswer No. ",i+1)
		print("\n",answers[i])
		if(comments[i] == 'none'):
			print("\n\nComments: none")
		else:
			print('\n\nComments:\n\n')
			for c in comments[i]:
				print(c,'\n')


def get_accepted_answer_comments(soup):
	# get accepted answer and comments on accepted answer if any
	accepted = soup.find(class_ = 'answer accepted-answer')
	if accepted:
		accepted_answer = cleanhtml(accepted.find(class_ = 'post-text').get_text())
		a_comments = accepted.find_all(class_ = 'comment-copy') # None if no comments
		accepted_comments  = []
		for a in a_comments:
			accepted_comments.append(cleanhtml(a.get_text()))
	return accepted_answer, accepted_comments


'''

# create list of answers and comments
answers,comments = get_answers_comments(soup)

# print answers and comments
print_answers_comments(answers,comments)

'''








