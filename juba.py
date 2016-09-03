# -*- coding : utf-8 -*-
#from __futue__ import import unicode_literals

host = '127.0.0.1'
port = 9199
name = 'test'

dirpath = "pet_dataset/images_partial/"

import sys, os
import json
import jubatus
from jubatus.common import Datum
import random

client = jubatus.Classifier(host,port,name)

def gen_datum(filename):
    with open(filename,"rb") as f:
        binary = f.read()
        d = Datum()
        d.add_binary( "image", binary)
    return d

def train():
    dirs = os.listdir(dirpath+"train/")
    train_data = []
    for dirname in dirs:
        files = os.listdir(dirpath+"train/"+dirname)
        for filename in files:
            train_data.append([dirname,gen_datum(dirpath+"train/"+dirname+"/"+filename)])
    random.shuffle(train_data)
    for entry in train_data:
        client.train([(entry[0],entry[1])])
        sys.stdout.write(".")
        sys.stdout.flush()

def test(dirname):
    OK = NG = 0
    print dirname
    files = os.listdir(dirpath+"test/"+dirname)
    for testfile in files:
        predict = client.classify([gen_datum(dirpath+"test/"+dirname+"/"+testfile)])
        predict = predict[0]
        # print predict[0].label, predict[0].score,predict[1].label,predict[1].score
        predict.sort(key=lambda x:x.score,reverse=True)
        if predict[0].label == dirname:
            OK += 1
            sys.stdout.write("o")
        else:
            NG += 1
            sys.stdout.write("x")
        sys.stdout.flush()
    print ""
    return OK,NG

print "train"
train()
print "test"
res0 = test("pug")
res1 = test("shibainu")
gOK = res0[0] + res1[0]
gNG = res0[1] + res1[1]
print gOK, gNG
print gOK*1.0/(gOK+gNG)
client.clear()
