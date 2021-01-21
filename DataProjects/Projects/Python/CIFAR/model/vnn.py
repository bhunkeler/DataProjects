import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, Flatten
# from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras import layers, models, regularizers, optimizers

from keras.layers.core import Lambda
from keras import backend as K
from keras import regularizers

class VNN:
    
    '''
    Reference:

    [1] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. 
    arXiv preprint arXiv:1409.1556, 2014. https://arxiv.org/pdf/1409.1556.pdf
    '''

    def __init__(self):

        print('init_vnn')
        self.__model = None
        self.__num_classes = 10
        self.__image_size = 28
        self.__num_channels = 3
        self.weight_decay = 0.0005
        self.x_shape = [32,32,3]
        
        '''
            if train:
                self.model = self.train(self.model)
            else:
                print('not applied')
            try: 
                path = os.path.dirname(os.path.abspath(__file__))
                pathname = os.path.join(path, 'VGG16_pretrained_cifar10.h5')
                self.model.load_weights(pathname)
        
            except OSError as err:
                print("OS error: {0}".format(err))
                
            except ValueError:
                print("Could not convert data to an integer.")
                
            except: 
                print("Unexpected error:", sys.exc_info()[0])
        '''


    def model(self):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3,3), activation = 'relu', input_shape=(self.__image_size, self.__image_size, self.__num_channels)))  
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(64, (3,3), activation = 'relu'))
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(64, (3,3), activation = 'relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation = 'relu'))
        model.add(layers.Dense(self.__num_classes, activation = 'softmax'))

        self.__model = model
        return model


    def train():
        md = self.__model
        print('train')    
        return md 

