# Written based on Newmu's Theano-Tutorial
# (https://github.com/Newmu/Theano-Tutorials)

import numpy
import os
path = os.path.dirname(os.path.abspath(__file__))
datasets_dir = path + "/mnist_data/"

# Creates 'one hot' arrays
def one_hot(x, n):
    if type(x) == list:
    	x = numpy.array(x)
    x = x.flatten()
    one_hot = numpy.zeros((len(x),n))
    one_hot[numpy.arange(len(x)),x] = 1
    return one_hot

# Loads the mnist database
def mnist(ntrain=60000, ntest=10000, onehot=True):
    data_dir = datasets_dir
    fd = open(os.path.join(data_dir, 'train-images.idx3-ubyte'))
    loaded = numpy.fromfile(file=fd, dtype=numpy.uint8)
    training_x = loaded[16:].reshape((60000,28*28)).astype(float)

    fd = open(os.path.join(data_dir, 'train-labels.idx1-ubyte'))
    loaded = numpy.fromfile(file=fd, dtype=numpy.uint8)
    training_y = loaded[8:].reshape((60000))

    fd = open(os.path.join(data_dir, 't10k-images.idx3-ubyte'))
    loaded = numpy.fromfile(file=fd, dtype=numpy.uint8)
    test_x = loaded[16:].reshape((10000,28*28)).astype(float)

    fd = open(os.path.join(data_dir, 't10k-labels.idx1-ubyte'))
    loaded = numpy.fromfile(file=fd, dtype=numpy.uint8)
    test_y = loaded[8:].reshape((10000))

    training_x = training_x/255.
    test_x = test_x/255.
    
    training_x = training_x[:ntrain]
    training_y = training_y[:ntrain]

    test_x = test_x[:ntest]
    test_y = test_y[:ntest]

    if onehot:
    	training_y = one_hot(training_y, 10)
    	test_y = one_hot(test_y, 10)
    else:
    	training_y = numpy.asarray(training_y)
    	test_y = numpy.asarray(test_y)
    return training_x, test_x, training_y, test_y

