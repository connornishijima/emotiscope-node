from nltk.util import ngrams

with open("sentiment_train_data","r") as f:
	data = f.read().split("\n")

outGrams = ""

for item in data:
	item = item.split("\t")
	sent = item[0]
	try:
		sentence = item[1]
	except:
		print "SKIP"
		pass

	n = 2
	bigrams = ngrams(sentence.split(), n)
	for gram in bigrams:
		outGrams+=sent
		outGrams+=","
		outGrams+=gram[0]
		outGrams+=" "
		outGrams+=gram[1]
		outGrams+="\n"

with open("sentiment_bigrams.lst","w") as f:
	f.write(outGrams)
