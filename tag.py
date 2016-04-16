from __future__ import division
import time
import nltk
import re

def extractAlphanumeric(InputString):
    from string import ascii_letters, digits
    return "".join([ch for ch in InputString if ch in (ascii_letters + digits + " ")])

def getMinimum(text):
	text = text.replace(";","")
	text = text.replace(":","")
	text = text.replace(",","")
	text = text.replace("!",".")
	text = text.replace("?",".")
	text = text.split(".")
	sents = []
	for sent in text:
		sent = sent.strip()
		sent = sent.lower()
		sent = extractAlphanumeric(sent)
		if len(sent) > 1:
			sents.append(sent)
	return sents

with open("sent_scores.txt","r") as f:
	data = f.read().split("\n")

sentScores = {}
for item in data:
	if len(item) > 1:
		item = item.split("\t")
		sentScores[item[0]] = int(item[1])

def getScore(input):
	pronouns = ["it","its","he","hes","hed","hell","she","shes","shed","shell"]
	negations = ["wont","cant","wouldnt","couldnt","not","isnt","no"]

	score = 0

	sents = getMinimum(input)
	outSents = set()

	termLast = False

	for sent in sents:
		for term in terms:
			first = sent.split(" ")[0]
			if first in pronouns:
				if termLast == True:
					termLast = False
					outSents.add(sent)
			if term in sent:
				termLast = True
				outSents.add(sent)
	
	sents = outSents
	print sents
	
	for item in sents:
		words = item.split(" ")
		lastWord = ""
		for word in words:
			try:
				if lastWord in negations:
					add = sentScores[word]*-1
				else:
					add = sentScores[word]
				score+=add
			except Exception as e:
				pass
			lastWord = word
	return score

terms = ["bernie","sanders"]

tweet = "Hillary Clinton and Bernie Sanders Spar On Health Care | MSNBC - https://t.co/43uQFFWsd7 https://t.co/cuxB2T9RUr"
print getScore(item)
