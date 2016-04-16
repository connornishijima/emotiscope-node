import os

os.chdir("/root")

os.system("rm archive.db")
os.system("rm *.pickle")
os.system("rm *.bak")

os.system("cp popular.default popular.json")
os.system("cp streamLevels.default streamLevels.json")

with open("tweet_stream.lst","w") as f:
	f.write("")

with open("current_score.txt","w") as f:
	f.write("0")

with open("master_score.txt","w") as f:
	f.write("0")

os.system("reboot")
