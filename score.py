import re

with open("sent_scores.txt","r") as f:
	scores = f.read().split("\n")

scoreData = {}
for item in scores:
	if len(item) > 1:
		item = item.split("\t")
		word = item[0]
		score = item[1]
		scoreData[word] = int(score)

def extractMinimum(text):
	text = text.lower()
	text = re.sub(r'\W+ ', '', text).replace("'","").replace('"','').replace(".","")
	return text

def classify(t):
	s = 0
	t = t.split(" ")
	for word in t:
		if word in scoreData:
			s+=scoreData[word]
	print s

text = "You're so scared you'll just say dumb shit."
classify(extractMinimum(text))
text = "I love the way Bernie is supporting the poverty-stricken. What a good guy."
classify(extractMinimum(text))
text = "I love you"
classify(extractMinimum(text))
text = "I hate you"
classify(extractMinimum(text))
