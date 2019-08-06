import requests
import re
from bs4 import BeautifulSoup
import pickle
import os
from flask import current_app

page = requests.get('https://stackoverflow.com/questions/7501947/understanding-pickling-in-python')
soup = BeautifulSoup(page.content, 'html.parser')


for ans in soup.find_all(class_='answer'):
	print(ans.find(class_='d-none',itemprop='name').get_text())
	if ans.find_all(class_='comment-user'):
		for c in ans.find_all(class_='comment-user'):
			print(c.get_text())
		print('\n')


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get_question_answers_comments(soup):
	question = cleanhtml(soup.find(class_= 'question-hyperlink').get_text())
	answers = []
	comments = []
	for ans in soup.find_all(class_ = 'answer'):
		if ans.find(class_='js-accepted-answer-indicator grid--item fc-green-500 ta-center p4'):
			continue
		text = cleanhtml(ans.find(class_='post-text').get_text())
		answers.append(text)
		if ans.find_all(class_='comment-copy'):
			temp = []
			for c in ans.find_all(class_='comment-copy'):
				text = cleanhtml(c.get_text())
				temp.append(text)
			comments.append(temp)
		else:
			comments.append('none') # 'none' if no comments
	return question, answers, comments


#get_question_answers_comments()
