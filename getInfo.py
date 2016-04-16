import json
import time
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

consumer_key="CAzXtcWQEsuWKklMGeBgA"
consumer_secret="v9NZyyb3w3dROxNbQBpHvyrQQ8V3VuEWeIM0VI6rSoc"
access_token="281156364-gZuWLYgrDe1mBRxlWcQAK4dnSAIRTBFSGaz5AZcd"
access_token_secret="z1Dvp40kj4XPb2hSexAyE0O2hBsF2kpsfumiNIDxI"

class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(consumer_key,consumer_secret)
api = tweepy.API(auth)

auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth,TweetListener())

while True:
	user = api.get_user('@BernieSanders')
	print user._json["profile_banner_url"]
	time.sleep(100)
