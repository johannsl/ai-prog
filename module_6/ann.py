# Written based on Newmu's Theano-Tutorial 
# (https://github.com/Newmu/Theano-Tutorials)
 
import load
import numpy
import theano
from theano import tensor
from theano.sandbox.rng_mrg import MRG_RandomStreams

# Constants
NUMBER_OF_RUNS = 10
INPUT_SIZE = 16
OUTPUT_SIZE = 4
LEARNING_RATE = 0.001
RHO = 0.9
EPSILON = 1e-6
BATCH_SIZE = 100

# Stream random number generator
srng = MRG_RandomStreams()

class ann():
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes

    # Activation functions
    def rectify(self, x):
        return tensor.maximum(x, 0.)
    
    def sigmoid(self, x):
        return tensor.nnet.sigmoid(x)
    
    def softmax(self, x):
        e_x = tensor.exp(x - x.max(axis=1).dimshuffle(0, 'x'))
        return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')
    
    # Help functions
    def float_x(self, x):
        return numpy.asarray(x, dtype=theano.config.floatX)
    
    def init_weights(self, shape):
        return theano.shared(self.float_x(numpy.random.randn(*shape) * 0.01))
    
    # Backpropagation functions
    def RMSprop(self, cost, params):
        grads = tensor.grad(cost=cost, wrt=params)
        updates = []
        for param, grad in zip(params, grads):
            accelerate = theano.shared(param.get_value() * 0.)
            accelerate_new = RHO * accelerate + (1 - RHO) * grad ** 2
            gradient_scaling = tensor.sqrt(accelerate_new + EPSILON)
            grad = grad / gradient_scaling
            updates.append((accelerate, accelerate_new))
            updates.append((param, param - LEARNING_RATE * grad))
        return updates
    
    def SGD(self, cost, params):
        grads = tensor.grad(cost=cost, wrt=params)
        updates = []
        for param, grad in zip(params, grads):
            updates.append([param, param - grad * LEARNING_RATE])
        return updates
    
    # Noise function
    def dropout(self, x, percent=0.):
        if percent > 0:
            retain_prob = 1 - percent
            x *= srng.binomial(
                            x.shape, 
                            p=retain_prob, 
                            dtype=theano.config.floatX)
            x /= retain_prob
        return x
    
    # The network models:
    # simple network with sigmoid activation;
    def model(self, x, weights, p_drop_input, p_drop_hidden):
        model_layer_values = []
        temp_layer_value = x
        for weight in weights[:-1]:
            layer_value = self.sigmoid(tensor.dot(temp_layer_value, weight))
            model_layer_values.append(layer_value)
            temp_layer_value = layer_value
        layer_value = self.softmax(tensor.dot(temp_layer_value, weights[-1]))
        model_layer_values.append(layer_value)
        return model_layer_values
    
    # advanced network with rec activation and noise;
    def model2(self, x, weights, p_drop_input, p_drop_hidden):
        model_layer_values = []
        x = self.dropout(x, p_drop_input)
        temp_layer_value = x
        for weight in weights[:-1]:
            layer_value = self.rectify(tensor.dot(temp_layer_value, weight))
            layer_value = self.dropout(layer_value, p_drop_hidden)
            model_layer_values.append(layer_value)
            temp_layer_value = layer_value
        layer_value = self.softmax(tensor.dot(temp_layer_value, weights[-1]))
        model_layer_values.append(layer_value)
        return model_layer_values
    
    # Load, init, and run function
    def main(self, silent=False):
        
        # Load training and test data
        training_x, test_x, training_y, test_y = load.game2048()
        
        # Symbolic variables
        x = tensor.fmatrix()
        y = tensor.fmatrix()
        
        # Initialize weights
        temp_weight = INPUT_SIZE
        weights = []
        for layer in self.layer_sizes:
            weight = self.init_weights((temp_weight, layer))
            weights.append(weight)
            temp_weight = layer
        weight = self.init_weights((temp_weight, OUTPUT_SIZE))
        weights.append(weight) 
        
        # Initialize model
        model_layer_noise = self.model2(x, weights, 0.2, 0.5)
        model_layer_values = self.model2(x, weights, 0., 0.)
        #y_x = tensor.argmax(model_layer_values[-1], axis=1)
        y_x = model_layer_values[-1]
        
        # Initialize the update function
        cost = tensor.mean(tensor.nnet.categorical_crossentropy(
                                                model_layer_noise[-1], y))
        params = weights
        updates = self.RMSprop(cost, params) # SGD / RMSprop

        # Initialize core functionality
        train = theano.function(
                        inputs=[x, y],
                        outputs=cost, 
                        updates=updates,
                        allow_input_downcast=True)
        self.predict = theano.function(
                        inputs=[x], 
                        outputs=y_x, 
                        allow_input_downcast=True)
        
        # Training on mnist
        if not silent: print("\nTRAINING...")
        for i in range(NUMBER_OF_RUNS):
            for start, end in zip(range(0, len(training_x), BATCH_SIZE),
                            range(BATCH_SIZE, len(training_x), BATCH_SIZE)):
                cost = train(training_x[start:end], training_y[start:end])
            if not silent: print("Iteration ", i+1, "/", NUMBER_OF_RUNS)
        

    # Run a blind test
    def blind_test(self, feature_sets):
        print("\nBLIND TESTING...")
        feature_sets = numpy.asarray(feature_sets)
        feature_sets = feature_sets/255.
        result = self.predict(feature_sets[0])
        result = result.tolist()
        print("Result: ", result)
        return result

    def predict_move(self, board):
        result = self.predict(board)
        return result[0] 

