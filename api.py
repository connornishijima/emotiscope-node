from __future__ import division
from flask import Flask, Response, render_template, jsonify, abort, make_response, request, send_from_directory
from flask.ext.cors import CORS
import json
import sqlite3
import time
import os
import pickle
import operator
import threading
from threading import Thread

os.chdir("/root")

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'EMOTISCOPE NODE'

@app.route('/info/<sec>')
def getInfo(sec):
	with open("config.json","r") as f:
		config = json.loads(f.read())
	with open("user_info.json","r") as f:
		user_info = json.loads(f.read())
	with open("info.json","r") as f:
		info = json.loads(f.read())
	with open("popular.json","r") as f:
		popular = json.loads(f.read())["popular"]

	secret = config["secret"]
	if sec == secret:
		wordCounts = {}
		try:
			with open('wordCounts.pickle', 'rb') as handle:
		                wordCounts = pickle.load(handle)
			os.system("cp wordCounts.pickle wordCounts.bak")
		except:
			try:
				os.system("cp wordCounts.bak wordCounts.pickle")
				with open('wordCounts.pickle', 'rb') as handle:
			                wordCounts = pickle.load(handle)
			except:
				pass
			pass
	
		badWords = []
		for item in wordCounts:
			if item[:4] == "http":
				badWords.append(item)
	
		for item in badWords:
			del wordCounts[item]
	
		data = {}
		data["email"] = config["email"]
		data["nickname"] = config["nickname"]
		data["campaign_id"] = config["campaign_id"]
		data["running"] = config["running"]
		data["api"] = config["api"]
		data["interval_minutes"] = config["interval_minutes"]

		data["top_words"] = info["top_words"]	
		data["days_left"] = info["days_left"]
		data["progress"] = info["progress"]
		data["end_time"] = info["end_time"]
	
		data["user"] = user_info
		data["user"]["screen_name"] = config["screen_name"]
	
		with open("tweetRanksSummary.json","r") as f:
			tweet_ranks_summary = json.loads(f.read())

		data["popular_users"] = tweet_ranks_summary
	
		tw = sorted(wordCounts.items(), key=operator.itemgetter(1))
		data["top_words"] = tw[::-1][:25]
	
		outWords = {}
	
		for item in data["top_words"]:
			word = item[0]
			count = item[1]
			outWords[word] = count
	
		with open('wordCounts.pickle', 'wb') as handle:
			pickle.dump(outWords, handle)
	
		return make_response(jsonify(data), 200)
	else:
		return make_response(jsonify({"error":"incorrect secret"}), 400)

@app.route('/archive/7', methods=['GET'])
def get7():
        conn = sqlite3.connect("archive.db")
        c = conn.cursor()

	tEnd = int(time.time())
	tStart = tEnd-604800

	outData = {"data":[]}

	c.execute("SELECT * FROM archive WHERE time > "+str(tStart)+" AND time < "+str(tEnd))
        data = c.fetchall()
	for item in data:
		pos = item[0]
		neg = item[1]
		score = item[3]
		unix = item[4]
		followers = item[5]
		if pos >= 0 and neg >= 0:
			outData["data"].append(
				{
					"pos":pos,
					"neg":neg,
					"score":score,
					"unix":unix,
					"followers":followers,
				}
			)

	return make_response(jsonify(outData), 200)

@app.route('/update', methods=['POST'])
def updateConfig():

	forbidden = ["campaign-id","end_time","running","start_time"]

	with open("config.json","r") as f:
		config = json.loads(f.read())

	secret = config["secret"]

	if request.form["secret"] == secret:
		bad_keys = []

		for item in request.form:
			if not item in forbidden:
				if item == "access_token":
					config["api"][item] = request.form[item]
				elif item == "access_token_secret":
					config["api"][item] = request.form[item]
				elif item == "consumer_key":
					config["api"][item] = request.form[item]
				elif item == "consumer_secret":
					config["api"][item] = request.form[item]
				elif item == "interval_minutes":
					config[item] = int(request.form[item])
				elif item in config:
					config[item] = request.form[item]
				else:
					print "'"+item+"' NOT IN CONFIG!"
			else:
				bad_keys.append(item)

		if len(bad_keys) == 0:
			with open("config.json","w") as f:
				f.write(json.dumps(config,indent=2,sort_keys=True))

			return make_response(jsonify({"status":"success"}), 200)
		else:
			return make_response(jsonify({"status":"error","reason":"Forbidden request!","keys":bad_keys}), 400)
	else:
		return make_response(jsonify({"status":"error","reason":"Incorrect secret"}), 400)

@app.route('/notifications', methods=['GET'])
def getNotifications():
	with open("notifications.lst","r") as f:
		notifications = f.read().splitlines(True)
	
	try:
		item = notifications[0]
	except IndexError:
		item = ""
	if len(item) > 1:
		item = item.split("%|%")
		text = item[0]
		type = item[1]
		timestamp = item[2]
	
		notification = {}
		notification["text"] = text
		notification["type"] = type
		notification["timestamp"] = timestamp
	else:
		notification = {}
		notification["text"] = "null"
		notification["type"] = "null"
		notification["timestamp"] = "null"

	with open("notifications.lst","w") as f:
		f.writelines(notifications[1:])

	return make_response(jsonify(notification), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True,threaded=True)
