from twython import TwythonStreamer
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
	    if not 'retweeted_status' in data:
	            tweet = data['text'].encode('utf-8').replace("\n"," ")
		    print tweet
	            nickname = data["user"]["name"].encode('utf-8')
	            handle = data["user"]["screen_name"].encode('utf-8')
	            with open("tweet_stream_live.lst","a+") as f:
	                    f.write(tweet+"\n")

    def on_error(self, status):
        print status

consumer_key="CAzXtcWQEsuWKklMGeBgA"
consumer_secret="v9NZyyb3w3dROxNbQBpHvyrQQ8V3VuEWeIM0VI6rSoc"
access_token="281156364-gZuWLYgrDe1mBRxlWcQAK4dnSAIRTBFSGaz5AZcd"
access_token_secret="z1Dvp40kj4XPb2hSexAyE0O2hBsF2kpsfumiNIDxI"

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

with open("config.json","r") as f:
	terms = json.loads(f.read())["terms"]

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
