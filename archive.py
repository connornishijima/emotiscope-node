from __future__ import division
import json
import time
import datetime
import sqlite3
import os
import tweepy
import pickle
#from tweepy import Stream
from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener

os.chdir("/root")

lastFollowerCount = 0
try:
	with open('followerFlowArray.pickle', 'rb') as handle:
		followerFlowArray = pickle.load(handle)
except:
	followerFlowArray = []

global milestonesHit
try:
	with open('milestonesHit.pickle', 'rb') as handle:
		milestonesHit = pickle.load(handle)
except:
	milestonesHit = []

conn = sqlite3.connect("archive.db")
c = conn.cursor()

with open("config.json","r") as f:
        config = json.loads(f.read())

consumer_key        = config["api"]["consumer_key"]
consumer_secret     = config["api"]["consumer_secret"]
access_token        = config["api"]["access_token"]
access_token_secret = config["api"]["access_token_secret"]

def notify(text,type):
	with open("notifications.lst","a+") as f:
		f.write(text+"%|%"+type+"%|%"+str(int(time.time())))

def getMilestone(number):
	global milestonesHit

	if len(milestonesHit) > 0:
	        lastMilestone = milestonesHit[-1]
	else:
		lastMilestone = 0

        MSB = int(str(number)[0])

        if MSB < 5:
                milestoneMSB = "5"
        else:
                milestoneMSB = "10"

        extra = len(str(number))-1
        milestone = int(milestoneMSB+("0"*extra))

        if number >= lastMilestone:
                if not lastMilestone in milestonesHit:
                        milestonesHit.append(lastMilestone)
                        lastMilestone = milestone
                        print "---------------------------------------!"

        try:
		if lastMilestone != 0:
	                percentage = int(( (number-milestonesHit[-1]) / (milestone-milestonesHit[-1]) )*100)
		else:
			percentage = int(( number / milestone )*100)
        except ZeroDivisionError:
		print "ZERO ERROR:"
		print number,milestone
                percentage = 0

        return milestone,percentage

def getETA(followerCount,followersPer,interval,milestone):
        now = int(time.time())
        left = int(milestone)-int(followerCount)
        seconds = left/(followersPer/interval/60)
        ETA = int(now+seconds)

	return ETA

while True:
	with open("config.json","r") as f:
	        config = json.loads(f.read())

	screen_name = config["screen_name"]

	interval = 60*config["interval_minutes"]

	if int(time.time()) % interval == 0:

		notify("Dataset updated!","GOOD")

		auth = OAuthHandler(consumer_key,consumer_secret)
		api = tweepy.API(auth)
		auth.set_access_token(access_token, access_token_secret)
		#twitterStream = Stream(auth,TweetListener())
		user = api.get_user(screen_name)

		user_data = {}

		user_data["screen_name"] = screen_name
		user_data["nickname"] = user.name
        	user_data["description"] = user.description
        	user_data["follower_count"] = user.followers_count
        	user_data["url"] = user.url
		user_data["banner_url"] = user._json["profile_banner_url"]
		user_data["status"] = user._json["status"]["text"]

		user_data["milestones"] = {}

		user_data["milestones"]["next"],user_data["milestones"]["percentage"] = getMilestone(int(user_data["follower_count"]))

		if lastFollowerCount != 0:
			flow = int(user_data["follower_count"]) - lastFollowerCount
		else:
			flow = 0

		lastFollowerCount = int(user_data["follower_count"])

		if len(followerFlowArray) > 10:
			del followerFlowArray[0]

		if flow != 0:
			followerFlowArray.append(flow)
		else:
			lastFollowerCount = int(user_data["follower_count"])

		if len(followerFlowArray) > 0:
			averageFollowerFlow = sum(followerFlowArray) / len(followerFlowArray)
			user_data["average_follower_flow"] = averageFollowerFlow

			if averageFollowerFlow > 0:
				print "followerCount followersPer interval milestone"
				print int(user_data["follower_count"]), averageFollowerFlow, config["interval_minutes"], user_data["milestones"]["next"]
				user_data["milestones"]["eta"] = str(getETA(int(user_data["follower_count"]), averageFollowerFlow, config["interval_minutes"], user_data["milestones"]["next"]))
			else:
				user_data["milestones"]["eta"] = "infinity"

		user_data["milestones"]["hit"] = milestonesHit

		print lastFollowerCount
		print followerFlowArray

		with open("user_info.json","w") as f:
			f.write(json.dumps(user_data,indent=2))

		with open("master_score.txt","r") as f:
			masterScore = int(f.read())

		with open("current_score.txt","r") as f:
			currentScore = int(f.read())

		with open("current_score.txt","w") as f:
			f.write("0")

		masterScore+=currentScore
		with open("master_score.txt","w") as f:
			f.write(str(masterScore))

		with open("streamLevels.json","r") as f:
			data = json.loads(f.read())
		
		with open("streamLevels.json","w") as f:
			f.write('{"pos":0,"neg":0,"neu":0}')
		
		data["time"] = int(time.time())
		data["score"] = masterScore
		print data

		c.execute("""CREATE TABLE IF NOT EXISTS
		        archive(
		                pos INT,neg INT,neu INT,score INT,time INT,followers INT
		        )
		""")

		c.execute('''INSERT INTO archive (
				pos,neg,neu,score,time,followers
			) VALUES (?,?,?,?,?,?)''',
			(
				data["pos"],data["neg"],data["neu"],data["score"],data["time"],user_data["follower_count"]
			)
		)

		conn.commit()

		with open('followerFlowArray.pickle', 'wb') as handle:
                        pickle.dump(followerFlowArray, handle)

	else:
		print time.time()
	
	time.sleep(1)

c.close()
conn.close()
