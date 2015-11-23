import load
import numpy
import theano
from theano import tensor
from theano.sandbox.rng_mrg import MRG_RandomStreams

# Constants
NUMBER_OF_RUNS = 100
LEARNING_RATE = 0.001
RHO = 0.9
EPSILON = 1e-6

# Stream random number generator
srng = MRG_RandomStreams()

def float_x(x):
    return numpy.asarray(x, dtype=theano.config.floatX)

def init_weights(shape):
    return theano.shared(float_x(numpy.random.randn(*shape) * 0.01))

def rectify(x):
    return tensor.maximum(x, 0.)

def softmax(x):
    e_x = tensor.exp(x - x.max(axis=1).dimshuffle(0, 'x'))
    return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

def RMSprop(cost, params):
    grads = tensor.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        acc = theano.shared(p.get_value() * 0.)
        acc_new = RHO * acc + (1 - RHO) * g ** 2
        gradient_scaling = tensor.sqrt(acc_new + EPSILON)
        g = g / gradient_scaling
        updates.append((acc, acc_new))
        updates.append((p, p - LEARNING_RATE * g))
    return updates

def dropout(x, p=0.):
    if p > 0:
        retain_prob = 1 - p
        x *= srng.binomial(x.shape, p=retain_prob, dtype=theano.config.floatX)
        x /= retain_prob
    return x

def model(x, weight_hidden, weight_hidden2, weight_out, p_drop_inumpyut, p_drop_hidden):
    x = dropout(x, p_drop_inumpyut)
    h = rectify(tensor.dot(x, weight_hidden))

    h = dropout(h, p_drop_hidden)
    h2 = rectify(tensor.dot(h, weight_hidden2))

    h2 = dropout(h2, p_drop_hidden)
    py_x = softmax(tensor.dot(h2, weight_out))
    return h, h2, py_x

# Training and test data; 
# x represents the data and y represents the correct response
training_x, test_x, training_y, test_y = load.game2048()

# Symbolic variables
x = tensor.fmatrix()
y = tensor.fmatrix()

#tada = len(training_x)

weight_hidden = init_weights((16, 600))
weight_hidden2 = init_weights((600, 600))
weight_out = init_weights((600, 4))

noise_h, noise_h2, noise_py_x = model(x, weight_hidden, weight_hidden2, weight_out, 0.2, 0.5)
h, h2, py_x = model(x, weight_hidden, weight_hidden2, weight_out, 0., 0.)

cost = tensor.mean(tensor.nnet.categorical_crossentropy(noise_py_x, y))
params = [weight_hidden, weight_hidden2, weight_out]
updates = RMSprop(cost, params)

# This is the core of the ann functionality
train = theano.function(inputs=[x, y], outputs=cost, updates=updates, allow_input_downcast=True)
predict = theano.function(inputs=[x], outputs=py_x, allow_input_downcast=True)

# Run training and testing
def run():
    numpy.set_printoptions(threshold=numpy.nan)
    #for i in range(NUMBER_OF_RUNS):
    n = 100
    for i in range(n):
        print("Training iteration", i+1, "of", n)
        for start, end in zip(range(0, len(training_x), 128),
                             range(128, len(training_y), 128)):
            cost = train(training_x[start:end], training_y[start:end])
        #print(numpy.mean(numpy.argmax(test_y, axis=1) == predict(test_x)))
        #print(test_y[0], predict(test_x)[0])
        #print(len(predict(test_x)))

def predict_move(board):
    #print("board", board)
    result = predict(board)
    #print("result", result)
    return result[0]
