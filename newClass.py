from __future__ import division
from nltk.util import ngrams
import time
from collections import Counter
import json

def classifySent(sentence):
	negScore = 0
	posScore = 0
	totalScore = 0

	n = 2
	bigrams = ngrams(sentence.split(), n)
	for gram in bigrams:
		gram = gram[0]+" "+gram[1]
		if gram in sentBigramsSet["neg"]:
			negScore+=sentBigramsOccur["neg"][gram]
		if gram in sentBigramsSet["pos"]:
			posScore+=sentBigramsOccur["pos"][gram]

	totalScore = posScore+negScore

	try:
		confidence = {
			"pos":(posScore/totalScore)*100,
			"neg":(negScore/totalScore)*100,
		}
	except ZeroDivisionError:
		confidence = {
			"pos":0,
			"neg":0,
		}
	return confidence

sentBigramsList = {
	"pos":[],
	"neg":[]
}
sentBigramsSet = {
	"pos":set(),
	"neg":set()
}

sentBigramsOccur = {
	"pos":{},
	"neg":{}
}

with open("sentiment_bigrams.lst","r") as f:
	data = f.read().split("\n")

l = len(data)
i = 0
for item in data:
	try:
		item = item.split(",")
		sent = item[0]
		bigram = item[1]
		sentBigramsList[sent].append(bigram)
		sentBigramsSet[sent].add(bigram)
	except:
		pass
	if i%10000==0:
		print (i/l)*100
	i+=1

sentBigramsOccur["pos"] = Counter(sentBigramsList["pos"])
sentBigramsOccur["neg"] = Counter(sentBigramsList["neg"])

while True:
	input = raw_input("Enter some text...")
	tStart = time.time()
	print json.dumps(classifySent(input),indent=2)
	tEnd = time.time()
	print tEnd-tStart
	print "\n"
