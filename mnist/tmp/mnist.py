import csv
import struct
def convert(imgf, labelf, outimgf,outlabelf, n):
	f = open(imgf,'rb')
	l = open(labelf,'rb')
	of = open(outimgf,'wb')
	ol = open(outlabelf,'w')

	f.read(16)
	l.read(8)
	images=[]
	labels=[]
	for i in range(n):
		labels.append(ord(l.read(1)))
		images.append(f.read(28*28))
		print type(images[0])
	#output img binary
	writer = csv.writer(of)
	writer.writerows(images)
	#output correct labels
	writer = csv.writer(ol)
	writer.writerow(labels)

	f.close()
	l.close()
	of.close()
	ol.close()

if __name__ == '__main__':
	convert("train-images-idx3-ubyte","train-labels-idx1-ubyte","train_data.csv","train_labels.csv",60000)
	convert("t10k-images-idx3-ubyte","t10k-labels-idx1-ubyte","test_data.csv","test_labels.csv",10000)