import theano
from theano import tensor
import numpy

from load import mnist

# Stream random number generator
srng = theano.sandbox.rng_mrg.MRG_RandomStreams()

def floatX(X):
    return numpy.asarray(X, dtype=theano.config.floatX)

def init_weights(shape):
    return theano.shared(floatX(numpy.random.randn(*shape) * 0.01))

def rectify(X):
    return tensor.maximum(X, 0.)

def softmax(X):
    e_x = tensor.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
    return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

def RMSprop(cost, params, learning_rate=0.001, rho=0.9, epsilon=1e-6):
    grads = tensor.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        acc = theano.shared(p.get_value() * 0.)
        acc_new = rho * acc + (1 - rho) * g ** 2
        gradient_scaling = tensor.sqrt(acc_new + epsilon)
        g = g / gradient_scaling
        updates.append((acc, acc_new))
        updates.append((p, p - learning_rate * g))
    return updates

def dropout(X, p=0.):
    if p > 0:
        retain_prob = 1 - p
        X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
        X /= retain_prob
    return X

def model(X, weight_hidden, weight_hidden2, weight_out, p_drop_inumpyut, p_drop_hidden):
    X = dropout(X, p_drop_inumpyut)
    h = rectify(tensor.dot(X, weight_hidden))

    h = dropout(h, p_drop_hidden)
    h2 = rectify(tensor.dot(h, weight_hidden2))

    h2 = dropout(h2, p_drop_hidden)
    py_x = softmax(tensor.dot(h2, weight_out))
    return h, h2, py_x

trX, teX, trY, teY = mnist(onehot=True)

X = tensor.fmatrix()
Y = tensor.fmatrix()

weight_hidden = init_weights((784, 625))
weight_hidden2 = init_weights((625, 625))
weight_out = init_weights((625, 10))

noise_h, noise_h2, noise_py_x = model(X, weight_hidden, weight_hidden2, weight_out, 0.2, 0.5)
h, h2, py_x = model(X, weight_hidden, weight_hidden2, weight_out, 0., 0.)
y_x = tensor.argmax(py_x, axis=1)

cost = tensor.mean(tensor.nnet.categorical_crossentropy(noise_py_x, Y))
params = [weight_hidden, weight_hidden2, weight_out]
updates = RMSprop(cost, params, learning_rate=0.001)

# This is the core of the ann functionality
train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)

# Run training and testing
def run():
    for i in range(100):
        for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
            cost = train(trX[start:end], trY[start:end])
        print(numpy.mean(numpy.argmax(teY, axis=1) == predict(teX)))

