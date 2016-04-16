import datetime
import json
import time
import sqlite3
import sys
import operator
import os

os.system("/root")

tNow = int(time.time())

conn = sqlite3.connect("archive.db")
c = conn.cursor()

c.execute("SELECT * FROM tweets")
data = c.fetchall()

tweets = []

i = 0
while i < len(data):
	followers = data[i][5]
	unix = data[i][6]

	rank = followers-(tNow-unix)

	tweets.append(
		[
			data[i][0], 		#tweet
			data[i][1],		#handle
			data[i][2],		#nickname
			int(data[i][3]),	#score
			data[i][4],		#class
			int(data[i][5]),	#followers
			int(data[i][6]),	#unix
			rank,
		]
	)
	i+=1

#print json.dumps(tweets,indent=2)

tweets.sort(key=operator.itemgetter(7))
tweets.reverse()

tweetRanks = []
tweetRanksSummary = []

for item in tweets:
	data = {}
	data["tweet"] = item[0]
	data["handle"] = item[1]
	data["nickname"] = item[2]
	data["score"] = item[3]
	data["class"] = item[4]
	data["followers"] = item[5]
	data["unix"] = item[6]
	data["rank"] = item[7]
	data["datetime"] = datetime.datetime.fromtimestamp(int(item[6])).strftime('%Y-%m-%d %H:%M:%S')
	tweetRanks.append(data)

for item in tweets[:50]:
	data = {}
	data["tweet"] = item[0]
	data["handle"] = item[1]
	data["nickname"] = item[2]
	data["score"] = item[3]
	data["class"] = item[4]
	data["followers"] = item[5]
	data["unix"] = item[6]
	data["rank"] = item[7]
	data["datetime"] = datetime.datetime.fromtimestamp(int(item[6])).strftime('%Y-%m-%d %H:%M:%S')
	tweetRanksSummary.append(data)


print json.dumps(tweetRanksSummary,indent=2)

with open("tweetRanks.json","w") as f:
	f.write(json.dumps(tweetRanks,indent=2))

with open("tweetRanksSummary.json","w") as f:
	f.write(json.dumps(tweetRanksSummary,indent=2))
