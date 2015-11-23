import numpy
import os
from math import log
path = os.path.dirname(os.path.abspath(__file__))
datasets_dir = path + "/training_data/"

def one_hot(x,n):
    if type(x) == list:
        x = numpy.array(x)
    x = x.flatten()
    o_h = numpy.zeros((len(x),n))
    o_h[numpy.arange(len(x)),x] = 1
    return o_h

def normalize(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] > 0: data[i][j] = log(data[i][j])
    return data

def game2048():
    files = os.listdir(datasets_dir)
    datas = []
    labels = []
    for f in files:
        data = numpy.loadtxt(
            os.path.join(datasets_dir, f),
            dtype=int,
            delimiter=' ',
            #unpack=True,
            usecols=range(16))
        data2 = numpy.loadtxt(
            os.path.join(datasets_dir, f),
            dtype=int,
            delimiter=' ',
            usecols=range(17))
        raw_labels = data2[:,16]
        #print("Shape of datas:", numpy.shape(data))
        #print("Shape of labels:", numpy.shape(raw_labels))
        #print("Raw labels:", raw_labels)
        labels2 = [[0 for y in range(4)] for x in range(len(raw_labels))]
        for i in range(len(raw_labels)):
           labels2[i][int(raw_labels[i])] = 1.0
        labbel = numpy.asarray(labels2)
        #print("labbel", labbel)
        #labbel = one_hot(labbel, 16)
        #print("HOT labbel", labbel)
        #data = normalize(data)
        datas.append(data)
        labels.append(labbel)
    trX = datas[0]# + datas[1]
    trY = labels[0]# + labels[1]
    #print(trX)
    #print(trY)
    return trX, trX, trY, trY

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
