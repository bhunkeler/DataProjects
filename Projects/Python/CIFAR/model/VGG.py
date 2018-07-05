from __future__ import print_function

import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras import layers, models, regularizers, optimizers

from keras.layers.core import Lambda
from keras import backend as K
from keras import regularizers

import numpy as np
import os
import sys

import utils

class VGG:
    
    '''
    Reference:

    [1] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. 
    arXiv preprint arXiv:1409.1556, 2014. https://arxiv.org/pdf/1409.1556.pdf
    '''
    # Constructor
    def __init__(self, input_shape = (32,32,3), num_classes = 10, weight_decay = 0.005):
        self.__num_classes  = num_classes
        self.__weight_decay = weight_decay
        self.__x_shape      = input_shape
        self.__model        = None 
                
    def build(self, datashape = (32, 32, 3), num_classes = 10, path = None):
        '''
        Build the network of vgg for 10 classes with 
        dropout and weight decay as described in the paper 2Very deep convolutional networks for 
        large-scale image recognition'

        param:  datashape   - shape of the imput data
                num_classes - number of classes to predict 
                path        - to pretrained model
                
        return: model instance
        '''
            
        weight_decay = 1e-4

        model = Sequential()
        model.add(layers.Conv2D(64, (3, 3), padding='same', input_shape = (48, 48, 3), activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.3))

        model.add(layers.Conv2D(64, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Conv2D(128, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(128, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())

        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Conv2D(256, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(256, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(256, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())

        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())

        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.4))

        model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())

        model.add(layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(layers.Dropout(0.5))

        model.add(layers.Flatten())
        model.add(layers.Dense(512,activation = 'relu', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(layers.BatchNormalization())

        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(num_classes, activation = 'softmax'))
        
    
        if path != None:
            # Loads ImageNet pre-trained data
            model.load_weights(path)

        return model

    def __normalize(self, data):
        
        '''
           this function normalize inputs for zero mean and unit variance

           param:  training and test dataset
           return: normalized data set
        '''

        mean      = np.mean(data, axis=(0, 1, 2, 3))
        std       = np.std(data,  axis=(0, 1, 2, 3))
        data_norm = (data - mean)/(std+1e-7)
        
        return data_norm

    def __normalize_production(self, x):
        
        '''
           this function is used to normalize instances in production according 
           to saved training set statistics

           param:  training dataset
           return: normalized data set
        '''
        # these values produced during first training and are general for the standard cifar10 training set normalization
        mean = 120.707
        std = 64.15
        return (x-mean)/(std+1e-7)

    def predict(self, x, batch_size = 50):
        
        x = self.__normalize(x)

        return self.__model.predict(x,batch_size)

    def train(self, x_train, y_train, x_val, y_val, x_test, y_test, batch_size = 128, max_epochs = 250, learning_rate = 0.1, learning_rate_decay = 1e-6):

        #training parameters
        batch_size = batch_size
        # maxepoches = max_epochs
        learning_rate = learning_rate
        learning_rate_decay = learning_rate_decay

        x_train = x_train.astype('float32')
        x_test  = x_test.astype('float32')
        x_train = self.__normalize(x_train)
        x_test  = self.__normalize(x_test)

        y_train = keras.utils.to_categorical(y_train, self.__num_classes)
        y_test = keras.utils.to_categorical(y_test, self.__num_classes)

        lrf = learning_rate

        datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range = 40,
            width_shift_range = 0.2,
            height_shift_range = 0.2,
            shear_range = 0.2,
            zoom_range = 0.2,
            horizontal_flip = True,
            fill_mode = 'nearest')

        datagen.fit(x_train)

        #optimization details
        sgd = optimizers.SGD(lr=lrf, decay = learning_rate_decay, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])

        # training process in a for loop with learning rate drop every 25 epoches.

        datagenerator = datagen.flow(x_train, y_train, batch_size=batch_size)
        history = model.fit_generator(datagenerator, 
                                      steps_per_epoch=x_train.shape[0] // batch_size,
                                      epochs = max_epochs,
                                      validation_data=(x_val, y_val),
                                      initial_epoch=max_epochs-1)

        model.save_weights('cifar10vgg.h5')
        return model

