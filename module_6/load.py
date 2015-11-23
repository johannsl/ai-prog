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
        data = normalize(data)
        datas.append(data)
        labels.append(labbel)
    trX = numpy.concatenate(datas)#datas[1]# + datas[1]
    trY = numpy.concatenate(labels)#labels[1]# + labels[1]
    #print(trX)
    #print(trY)
    return trX, trX, trY, trY
