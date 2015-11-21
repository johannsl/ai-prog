import numpy
import os
path = os.path.dirname(os.path.abspath(__file__))
datasets_dir = path + "/mnist_data/"

def one_hot(x,n):
	if type(x) == list:
		x = numpy.array(x)
	x = x.flatten()
	o_h = numpy.zeros((len(x),n))
	o_h[numpy.arange(len(x)),x] = 1
	return o_h

def mnist(ntrain=60000,ntest=10000,onehot=True):
	data_dir = datasets_dir
	fd = open(os.path.join(data_dir,'train-images.idx3-ubyte'))
	loaded = numpy.fromfile(file=fd,dtype=numpy.uint8)
	trX = loaded[16:].reshape((60000,28*28)).astype(float)

	fd = open(os.path.join(data_dir,'train-labels.idx1-ubyte'))
	loaded = numpy.fromfile(file=fd,dtype=numpy.uint8)
	trY = loaded[8:].reshape((60000))

	fd = open(os.path.join(data_dir,'t10k-images.idx3-ubyte'))
	loaded = numpy.fromfile(file=fd,dtype=numpy.uint8)
	teX = loaded[16:].reshape((10000,28*28)).astype(float)

	fd = open(os.path.join(data_dir,'t10k-labels.idx1-ubyte'))
	loaded = numpy.fromfile(file=fd,dtype=numpy.uint8)
	teY = loaded[8:].reshape((10000))

	trX = trX/255.
	teX = teX/255.

	trX = trX[:ntrain]
	trY = trY[:ntrain]

	teX = teX[:ntest]
	teY = teY[:ntest]

	if onehot:
		trY = one_hot(trY, 10)
		teY = one_hot(teY, 10)
	else:
		trY = numpy.asarray(trY)
		teY = numpy.asarray(teY)

	return trX,teX,trY,teY
