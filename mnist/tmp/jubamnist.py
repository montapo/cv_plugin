import numpy as np
import csv
import jubatus 
from jubatus.common import Datum

host = '127.0.0.1'
port = 9199
name = 'test'
client = jubatus.Classifier(host,port,name)

def get_labels(path):
	with open(path,"rb") as f:
		reader = csv.reader(f)
		for row in reader:
			labels = row
	return labels

def get_traindata(labels,data):
	traindata = []
	with open(data,"rb") as f:
		for i in range(len(labels)):
			binary = f.read(28*28)
			d = Datum()
			d.add_binary("image",binary)
			traindata.append([labels[i],d])
		# reader = csv.reader(f)
		# for i,row in enumerate(reader):
		# 	print row 	
		# 	d = Datum()
		# 	d.add_binary("image",row)
		# 	traindata.append([labels[i],d])
	print "num of train data :",len(traindata)
	return traindata

def get_testdata(labels,data):
	testdata = []
	with open(data,"rb") as f:
		for i in range(len(labels)):
			binary = f.read(28*28)
			d = Datum()
			d.add_binary("image",binary)
		# reader = csv.reader(f)
		# for row in reader:
		# 	d = Datum()
		# 	d.add_binary("image",row)
			testdata.append([d])
	print "num of test  data :",len(testdata)
	return testdata

def train(traindata):
	for entry in traindata:
		client.train([(entry[0],entry[1])])
		sys.stdout.write(".")
		sys.stdout.flush()

def test(testdata,labels):
	OK = NG = 0
	for test,label in zip(testdata,labels):
		predict = client.classify(test)
		predict = predict[0]
		predict.sort(key=lambda x:x.score, reverse=True)
		if predict[0].label == label:
			OK += 1
			sys.stdout.write("o")
		else:
			NG += 1
			sys.stdout.write("x")
		sys.stdout.flush()
	print ""
	Accuracy = OK*1.0/(OK+NG)
	print "OK : %d, NG :%d, Accuracy : %f"%(OK,NG,Accuracy)





if __name__ == '__main__':
	# traindata = get_traindata("mnist_train.csv")
	# testdata,labels = get_testdata("mnist_test.csv")
	# train(traindata)
	# test(testdata,labels)
	train_labels = get_labels("train_labels.csv")
	train_data = get_traindata(train_labels, "train_data.csv")
	test_labels = get_labels("test_labels.csv")
	test_data = get_testdata(test_labels,"test_data.csv")
	train(train_data)
	test(test_data,labels)