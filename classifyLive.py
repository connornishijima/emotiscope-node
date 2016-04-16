from itertools import chain
from websocket import create_connection
from libshorttext.classifier import *
import traceback
import re
import time
import json
import pickle
import os

os.chdir("/root")

connected = False
while connected == False:
	try:
		ws = create_connection("ws://plus.emotiscope.co:8000/ws")
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

with open("stops.lst","r") as f:
	stops = f.read().split("\n")

def getSentScore(t):
	s = 0
        t = t.split(" ")
        for word in t:
                if word in scoreData:
                        s+=scoreData[word]
        return s

def classifyTextModel(item):
        ret = predict_single_text(item, sub_mod)
        sub_result = str(ret).replace("unanalyzable result: ","")
        if sub_result == "sub":
                ret = predict_single_text(item, sent_mod)
                sent_result = str(ret).replace("unanalyzable result: ","")
        else:
                sent_result = "neu"
        return sent_result

def getWords(s):
	for word in s:
		try:
			if word[0] != "@":
				if word[0] != "#":
					if len(word) >= 3:
						if not word in common:
							try:
								wordCounts[word]+=1
							except:
								wordCounts[word]=1
		except:
			pass

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

with open("current_score.txt","r+") as f:
	currentScore = int(f.read())

while True:
	try:
		with open("tweet_stream_live.lst","r") as f:
			tweets = f.read().split("\n")
		with open("tweet_stream_live.lst","w") as f:
			f.write("")
		for item in tweets:
			tweet = item
			minimum = re.sub(r'\W+ ', '', tweet).replace("'","").replace('"','')
			minimum = re.sub(r"http\S+", "", minimum).lower()
			outMin = ""
			for word in minimum.split(" "):
				if word[:2] != "rt":
					if word[:1] != "#":
						if word[:1] != "@":
							if not word in stops:
								outMin+=word
								outMin+=" "
			minimum = outMin[:-1]
			print "================================"
			print minimum
			c = classifyTextModel(minimum)
			score = 0
			if c != "neu":
				score = getSentScore(minimum)
			counts[c]+=1
			totalCount+=1
			print c
			print score
			answer = raw_input("Was this correct? (y/n)")
			if answer == "y":
				pass
			elif answer == "n":
				answer = raw_input("What was the real class? (pos/neg/neu)")
				if answer == "pos" or answer == "neg":
					sub = "sub"
					sent = answer
					with open("sentiment_train_data","a+") as f:
						f.write(sent+"\t"+minimum+"\n")
					with open("subjectivity_train_data","a+") as f:
						f.write(sub+"\t"+minimum+"\n")
				elif answer == "neu":
					sub = "obj"
					with open("subjectivity_train_data","a+") as f:
						f.write(sub+"\t"+minimum+"\n")
	except:
		traceback.print_exc()

	time.sleep(0.1)
