with open("sentiment_train_data","r") as f:
	data = f.read().split("\n")

outData = ""

for item in data:
	words = item.split(" ")
	if len(words) >= 10:
		outData+=item
		outData+="\n"

with open("sentiment_train_trim","w") as f:
	f.write(outData)
