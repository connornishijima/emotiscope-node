import os
import sys

os.chdir("/root")


try:
	test = sys.argv[1]
except:
	os.system("pkill -9 python && python runAll.py go")

os.system("python stream.py&")
os.system("python classify.py&")
os.system("python archive.py&")
os.system("python api.py")
