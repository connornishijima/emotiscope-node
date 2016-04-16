#from twython import TwythonStreamer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
import traceback
import sys

os.chdir("/root")

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, d):
        data = json.loads(d)
	if 'text' in data:
#	    if not "retweeted_status" in data:
            tweet = data['text'].encode('utf-8').replace("\n"," ")
	    print tweet
            nickname = data["user"]["name"].encode('utf-8')
            handle = data["user"]["screen_name"].encode('utf-8')
	    follower_count = data["user"]["followers_count"]
	    with open("popular.json","r") as f:
		popular = json.loads(f.read())
	    topOther = {}
	    topCount = 0
	    for item in popular["popular"]["others"]:
		otherCount = item["follower_count"]
		if otherCount >= topCount:
			topCount = otherCount
			topOther = item
	    if follower_count >= popular["popular"]["king"]["follower_count"]:
		popular["popular"]["others"].append(popular["popular"]["king"])
		popular["popular"]["king"] = {"follower_count":follower_count,"nickname":nickname,"handle":handle,"tweet":tweet}
		print "NEW KING:"
		with open("popular.json","w") as f:
			f.write(json.dumps(popular,indent=2))
	    elif follower_count >= topOther["follower_count"]:
		popular["popular"]["others"].append({"follower_count":follower_count,"nickname":nickname,"handle":handle,"tweet":tweet})
		with open("popular.json","w") as f:
			f.write(json.dumps(popular,indent=2))
            with open("tweet_stream.lst","a+") as f:
                    f.write(tweet+"%|%"+nickname+"%|%"+handle+"%|%"+str(follower_count)+"\n")

    def on_error(self, status):
        print status

with open("config.json","r") as f:
	config = json.loads(f.read())

terms = config["terms"]

consumer_key        = config["api"]["consumer_key"]
consumer_secret     = config["api"]["consumer_secret"]
access_token        = config["api"]["access_token"]
access_token_secret = config["api"]["access_token_secret"]

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

while True:
        try:
            stream = Stream(auth, l)

            #This line filter Twitter Streams to capture data by our current wordList
            stream.filter(track=terms,languages=["en"])
        except:
            print "FUCK: "
            traceback.print_exc()
            sys.exit()

        time.sleep(1)
