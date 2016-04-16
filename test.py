from libshorttext.classifier import *
import time
import os

os.chdir("/root")

def classifyTextModel(item):
        ret = predict_single_text(item, sub_mod)
        sub_result = str(ret).replace("unanalyzable result: ","")
        if sub_result == "sub":
                ret = predict_single_text(item, sent_mod)
                sent_result = str(ret).replace("unanalyzable result: ","")
        else:
                sent_result = "neu"
        print sent_result

print "START"

global sent_mod
sent_mod = TextModel('sentiment_model')

global sub_mod
sub_mod = TextModel('subjectivity_model')

tStart = time.time()
classifyTextModel("really liked outcome it was great")
tEnd = time.time()
print tEnd-tStart

tStart = time.time()
classifyTextModel("really liked outcome it was great")
tEnd = time.time()
print tEnd-tStart

tStart = time.time()
classifyTextModel("this movie was awful i hate the director")
tEnd = time.time()
print tEnd-tStart

tStart = time.time()
classifyTextModel("she goes around")
tEnd = time.time()
print tEnd-tStart

