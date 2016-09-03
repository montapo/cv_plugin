#coding: utf-8
import numpy as np
import csv
import pylab
from sklearn.datasets import fetch_mldata
from PIL import Image

mnist = fetch_mldata('MNIST original', data_home=".")
print len(mnist.data)
labels = []

# create data file
p = np.random.random_integers(0, len(mnist.data)-1, 7000)
for index, (data, label) in enumerate(np.array(zip(mnist.data, mnist.target))[p]):
	# pylab.axis('off')
	Image.fromarray(data.reshape(28,28)).save("mldata/"+str(index)+".jpg")
	# pylab.imshow(data.reshape(28, 28), cmap=pylab.cm.gray_r, interpolation='nearest')
	# pylab.savefig("mldata/"+str(index)+".jpg")
	# pylab.clf()
	labels.append([index,label])
	print index,label

with open("mldata/labels.csv","wb") as f:
	writer = csv.writer(f)
	writer.writerows(labels)