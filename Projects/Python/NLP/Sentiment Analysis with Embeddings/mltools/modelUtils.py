import keras
from keras import optimizers

class modelUtils:
    
    '''
    Reference:

    
    '''
    # Constructor
    def __init__(self, usage = False):
        
        if usage:
            print('Available optimizers: rmsprop, sgd, Adagrad, Adam, Adamax, Nadam ')

        print('initialized')

    def optimizer(self, optimizerType = 'rmsprop', default = True, learningrate = 1e4, learningrate_decay = 0.05):
        
        if default:
            if optimizerType == 'rmsprop':
                opt = optimizers.RMSprop(lr = 0.001, rho = 0.9, epsilon = None, decay = 0.0)

            if optimizerType == 'sgd':
                opt = optimizers.SGD(lr = 0.01, momentum = 0.0, decay = 0.0, nesterov = False)
                
            if optimizerType == 'Adagrad':
                opt = optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)

            if optimizerType == 'Adam':
                opt = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            
            if optimizerType == 'Adamax':
                opt = optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)

            if optimizerType == 'Nadam':
                opt = optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
        else:
            if optimizerType == 'rmsprop':
                opt = optimizers.RMSprop(lr = learningrate, rho = 0.9, epsilon = None, decay = 0.0)

            if optimizerType == 'sgd':
                opt = optimizers.SGD(lr = learningrate, decay = learningrate_decay, momentum = 0.9, nesterov = True)
                
            if optimizerType == 'Adagrad':
                opt = optimizers.Adagrad(lr = learningrate, epsilon=None, decay = learningrate_decay)

            if optimizerType == 'Adam':
                opt = optimizers.Adam(lr = learningrate, beta_1=0.9, beta_2=0.999, epsilon=None, decay = learningrate_decay, amsgrad=False)
            
            if optimizerType == 'Adamax':
                opt = optimizers.Adamax(lr = learningrate, beta_1=0.9, beta_2=0.999, epsilon=None, decay = learningrate_decay)

            if optimizerType == 'Nadam':
                opt = optimizers.Nadam(lr = learningrate, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay = learningrate_decay)           



        return opt