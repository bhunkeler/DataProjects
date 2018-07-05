import keras
from keras import optimizers

def optimizer(optimizerType = 'rmsprop', learning_rate = 1e-4, learning_rate_decay = 0.05):
    
    if optimizerType == 'rmsprop':
        opt = optimizers.RMSprop(lr = learning_rate)

    if optimizerType == 'sgd':
        opt = optimizers.SGD(lr = learning_rate, decay = learning_rate_decay, momentum = 0.9, nesterov = True)
        
    if optimizerType == 'adam':
        opt = optimizers.adam(lr = learning_rate, decay = learning_rate_decay, momentum = 0.9, nesterov = True)
        
    return opt