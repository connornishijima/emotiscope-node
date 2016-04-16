from __future__ import division
import datetime
import json
import random
import time

global lastMilestone
lastMilestone = 0

milestonesHit = []

def getMilestone(number):
	global lastMilestone
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
		percentage = int(( (number-milestonesHit[-1]) / (milestone-milestonesHit[-1]) )*100)
	except ZeroDivisionError:
		percentage = 0

	return number,milestone,percentage,milestonesHit

def getETA(followerCount,followersPer,interval,milestone):
        now = int(time.time())
        left = int(milestone)-int(followerCount)
        seconds = left/(followersPer/interval/60)
        ETA = int(now+seconds)

	print(
	    datetime.datetime.fromtimestamp(
	        int(ETA)
	    ).strftime('%Y-%m-%d %H:%M:%S')
	)

        year = divmod(ETA-now,1*60*60*24*30*12)  # years
        mon = divmod(year[1],1*60*60*24*30)  # months
        d = divmod(mon[1],1*60*60*24)  # days
        h = divmod(d[1],1*60*60)  # hours
        m = divmod(h[1],1*60)  # minutes
        s = m[1]  # seconds

        data = {
                "1 years":year,
                "2 months":mon,
                "3 days":d,
                "4 hours":h,
                "5 minutes":m,
                "6 seconds":s
        }

        return data

print json.dumps(getETA(1955738,35,5,5000000),indent=True,sort_keys=True)

#count = 0

#while True:
#	count+=random.randint(0,9)
#	print getMilestone(count);
