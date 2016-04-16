#Import the necessary methods from tweepy library
import traceback
import os
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys
import urllib2

#Variables that contains the user credentials to access Twitter API
access_token = "343884613-VXqJpZflKDyHN1ZXhfd7Nm0GMSljlYx0pYtwYG6L"
access_token_secret = "oLnqQXLhSoVaR5C6GUoiamkaXunTXMpmzxbki9Ll1nSFU"
consumer_key = "KeQserma3AmlYNkPEswBAzp4I"
consumer_secret = "1rPm9oabIAqOWxpJ9eU7dm4Z2jo6AwkLPZeOnDlmxjvWxDYOMZ"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        decoded = json.loads(data)

        global tList
        global tStart

	try:
                tweet = decoded["text"].encode('ascii', 'ignore').replace("\n"," ")
                print tweet
        except:
#               traceback.print_exc()
                pass

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    while True:
        try:
            stream = Stream(auth, l)

            #This line filter Twitter Streams to capture data by our current wordList
            stream.filter(track=["bernie"],languages=["en"])
        except:
            print "FUCK: "
            traceback.print_exc()
            sys.exit()

        time.sleep(1)

