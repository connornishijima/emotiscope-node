from __future__ import division
import time
import json
import os
import sys
import datetime
#sys.stdout = open('/root/checkProgress.log', 'w')

os.chdir("/root")

def send_email(subject, body, recipient):
    import smtplib

    user = "emotiscope"
    pwd = "employeE13]0813"

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

with open("lastEnd.txt","r") as f:
	lastEnd = int(f.read())
with open("config.json","r") as f:
	config = json.loads(f.read())
with open("info.json","r") as f:
	info = json.loads(f.read())

with open("warningTimes.json","r") as f:
	warnings = json.loads(f.read())

email = config["email"]

start_time = config["start_time"]
end_time = config["end_time"]
now_time = int(time.time())

start = 0
now = (now_time-start_time)+60
end = end_time-start_time

info["days_left"] = int((end_time-now_time)/86400)
info["end_time"] = end_time

seconds_left = end_time - now_time
if seconds_left < 86400:
	if not end_time in warnings["times"]:
		warnings["times"].append(end_time)
		with open("warningTimes.json","w") as f:
			f.write(json.dumps(warnings,indent=2))
		send_email("Your Emotiscope+ campaign ends soon!","You campaign will end in 24 hours at "+datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d %H:%M')+" (EST). EXTEND NOW!",email)

progress = (now/end)*100

print seconds_left
print now
print end
print progress

info["progress"] = float("{0:.2f}".format(progress))

if int(end_time) != int(lastEnd):
	send_email("Your Emotiscope+ campaign has been extended.","You campaign will now end at "+datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d %H:%M')+" (EST).",email)
	print "END TIME UPDATED"
	config["running"] = True
	with open("info.json","w") as f:
		f.write(json.dumps(info,indent=2))
	with open("config.json","w") as f:
		f.write(json.dumps(config,indent=2,sort_keys=True))
	with open("lastEnd.txt","w") as f:
		f.write(str(end_time))
	os.system("sudo reboot")
else:
	print "END TIME SAME"

if progress >= 100:
	info["progress"] = 100
	if config["running"] == True:
		print "CAMPAIGN OVER"
		send_email("Your Emotiscope+ campaign has ended.","Be sure to renew within 3 days!",email)
		config["running"] = False
		with open("info.json","w") as f:
			f.write(json.dumps(info,indent=2))
		with open("config.json","w") as f:
			f.write(json.dumps(config,indent=2,sort_keys=True))
	
		os.system("pkill -9 python && python api.py")

with open("info.json","w") as f:
	f.write(json.dumps(info,indent=2))

with open("config.json","w") as f:
	f.write(json.dumps(config,indent=2,sort_keys=True))

sys.exit(1)
