# -*- coding: utf-8 -*-

from itertools import chain
from websocket import create_connection
from libshorttext.classifier import *
import traceback
import sqlite3
import re
import time
import json
import pickle
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

os.chdir("/root")

conn = sqlite3.connect("archive.db")
c = conn.cursor()

connected = False
while connected == False:
	try:
		ws = create_connection("ws://emotiscope.co:8000/ws")
		connected = True
	except:
		print "STILL CONNECTING..."
		time.sleep(1)
		pass

try:
	with open('wordCounts.pickle', 'rb') as handle:
		wordCounts = pickle.load(handle)
except:
	wordCounts = {}

with open("common.lst","r") as f:
	common = f.read().split("\n")

with open("sent_scores.txt","r") as f:
        scores = f.read().split("\n")

scoreData = {}
for item in scores:
        if len(item) > 1:
                item = item.split("\t")
                word = item[0]
                score = item[1]
                scoreData[word] = int(score)

def getSentScore(t):
	s = 0
        t = t.split(" ")
        for word in t:
                if word in scoreData:
                        s+=scoreData[word]
        return s

def classifySubjectivity(item):
        ret = predict_single_text(item, sub_mod)
        sub_result = str(ret).replace("unanalyzable result: ","")
        return sub_result

def classifySentiment(item):
        ret = predict_single_text(item, sent_mod)
        sent_result = str(ret).replace("unanalyzable result: ","")
        return sent_result

def getWords(s):
	for word in s:
		try:
			if word[0] != "@":
				if word[0] != "#":
					if len(word) > 3:
						if not word in common:
							try:
								wordCounts[word]+=1
							except:
								wordCounts[word]=1
		except:
			pass

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
			if term in sent or term+"s" in sent:
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

def getMinimumString(text):
	text = text.replace(";","")
	text = text.replace(":","")
	text = text.replace(",","")
	text = text.replace("!",".")
	text = text.replace("?",".")
	text = text.strip()
	text = text.lower()
	text = extractAlphanumeric(text)
	return text

def archiveTweet(tweet,handle,nickname,score,cl,followers):

	tweet = unicode(tweet)
	handle = unicode(handle)
	nickname = unicode(nickname)
	cl = unicode(cl)

	unix = int(time.time())
	c.execute('''INSERT INTO tweets (
			tweet,handle,nickname,score,class,followers,unix
        	) VALUES (?,?,?,?,?,?,?)''',
        	(
			tweet,handle,nickname,score,cl,followers,unix
		)
	)

	conn.commit()

print "START"

totalCount = 0
counts = {
	"pos":0,
	"neg":0,
	"neu":0
}
defaultCounts = {
	"pos":0,
	"neg":0,
	"neu":0
}

global sent_mod
sent_mod = TextModel('sentiment_model')

global sub_mod
sub_mod = TextModel('subjectivity_model')

lastUpdate = 0
lastScoreCheck = 0

with open("current_score.txt","r+") as f:
	currentScore = int(f.read())

with open("config.json","r") as f:
	data = json.loads(f.read())

terms = data["terms"]
good_hashtags = data["good_hashtags"]
bad_hashtags = data["bad_hashtags"]
campaign_id = data["campaign_id"]

with open("sent_scores.txt","r") as f:
	data = f.read().split("\n")

sentScores = {}
for item in data:
	if len(item) > 1:
		item = item.split("\t")
		sentScores[item[0]] = int(item[1])

c.execute("""CREATE TABLE IF NOT EXISTS
	tweets(
		tweet TEXT, handle TEXT, nickname TEXT, score INT, class TEXT, followers INT, unix INT
	)
""")

while True:
	try:
		with open("tweet_stream.lst","r+") as f:
			data = f.read().split("\n")
		with open("tweet_stream.lst","w+") as f:
			f.write("")
		
		for item in data:
			if len(item) > 1:
				print "------------------!"
				item = item.split("%|%")
				tweet = item[0]
				nickname = item[1]
				handle = item[2]
				follower_count = int(item[3])
				minimum = getMinimumString(tweet)
				sub = classifySubjectivity(minimum)
				score = 0
				cl = "neu"
				print sub
				if sub != "obj":
					score = getScore(tweet)
#					sent_libsvm = classifySentiment(minimum)
#					if sent_libsvm == "pos":
#						score+=1
#					elif sent_libsvm == "neg":
#						score-=1

					if score != 0:
						if score < 0:
							cl = "neg"
						elif score > 0:
							cl = "pos"

					for tag in good_hashtags:
						if tag.decode('utf-8') in tweet.decode('utf-8'):
							print "\n\n\nFOUND GOOD TAG: "+tag
							cl = "pos"
							score+=1
					for tag in bad_hashtags:
						if tag.decode('utf-8') in tweet.decode('utf-8'):
							print "\n\n\nFOUND BAD TAG: "+tag
							cl = "neg"
							score-=1

					print score
					currentScore+=score

					getWords(minimum.split(" "))
					if time.time()-lastUpdate > 0.5:
						try:
							ws.send(str("NEW_TWEET%|%"+campaign_id+"%|%"+tweet+"%|%"+cl+"%|%"+nickname+"%|%"+handle).encode('utf-8'))
						except:
							print "NON-ASCII WS TWEET!"
						lastUpdate = time.time()

				archiveTweet(tweet,handle,nickname,score,cl,follower_count)

				counts[cl]+=score
				totalCount+=1
				print cl
				print "///////////////////"
				print "------------------!"

		print "CURRENT SCORE:\t"+str(currentScore)
	
		with open("streamLevels.json","r") as f:
			levels = json.loads(f.read())
		for i in levels:
			if counts[i] >= 0:
				levels[i]+=counts[i]
			else:
				levels[i]+=(counts[i]*-1)

		with open("streamLevels.json","w") as f:
			f.write(json.dumps(levels,indent=2))

		with open("current_score.txt","r") as f:
			lastScore = int(f.read())

		newScore = str(lastScore+currentScore)
		print "NEW SCORE:\t"+newScore

		with open("current_score.txt","w") as f:
			f.write(str(newScore))

		currentScore = 0
	
		counts["pos"] = defaultCounts["pos"]
		counts["neg"] = defaultCounts["neg"]
		counts["neu"] = defaultCounts["neu"]
	
		with open('wordCounts.pickle', 'wb') as handle:
			pickle.dump(wordCounts, handle)
	except:
		print "FUCK!"
		traceback.print_exc()
		try:
			ws = create_connection("ws://emotiscope.co:8000/ws")
		except:
			print "FUCK!"
			traceback.print_exc()

	time.sleep(5)
