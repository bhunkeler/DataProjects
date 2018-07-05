import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, Flatten
# from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras import layers, models, regularizers, optimizers

def model_simple(datashape = (32, 32, 3), num_classes = 10, path = None):
    
    model = Sequential()

    # Block 1
    model.add(layers.Conv2D(96, (3, 3), activation='relu', padding = 'same', input_shape = datashape))    
    model.add(layers.Dropout(0.2))
    model.add(layers.Conv2D(96, (3, 3), activation='relu', padding = 'same'))  
    model.add(layers.Conv2D(96, (3, 3), activation='relu', padding = 'same', strides = 2))    
    model.add(layers.Dropout(0.5))
    
    # Block 2
    model.add(layers.Conv2D(192, (3, 3), activation='relu', padding = 'same'))    
    model.add(layers.Conv2D(192, (3, 3), activation='relu', padding = 'same'))
    model.add(layers.Conv2D(192, (3, 3), activation='relu', padding = 'same', strides = 2))    
    model.add(layers.Dropout(0.5))    
    
    # Block 3
    model.add(layers.Conv2D(192, (3, 3), activation='relu', padding = 'same'))
    model.add(layers.Conv2D(192, (1, 1), activation='relu', padding = 'valid'))

    # Block 4
    # this final layer gave us about 82% accuracy 
    model.add(layers.Conv2D(num_classes, (1, 1), padding='valid'))
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Activation('softmax'))

    # this final layer gave us about 75% accuracy
    # model.add(layers.Flatten())
    # model.add(layers.Dense(192, activation = 'relu'))
    # model.add(layers.Dropout(0.5))
    # model.add(layers.Dense(num_classes, activation = 'softmax'))

    return model

def model_VGG16(datashape = (32, 32, 3), num_classes = 10, path = None):
    
    '''
    Build the network of vgg for 10 classes with 
    dropout and weight decay as described in the paper 2Very deep convolutional networks for 
    large-scale image recognition'

    Model Schema is based on 
    https://arxiv.org/abs/1409.1556
       
    Batch Normalization: 
    https://arxiv.org/abs/1502.03167

    ImageNet Pretrained Weights 
    https://drive.google.com/file/d/0Bz7KyqmuGsilT0J5dmRCM0ROVHc/view?usp=sharing

    param:  datashape   - shape of the imput data
            num_classes - number of classes to predict 
            path        - to pretrained model
            
    return: model instance
    '''
        
    model = Sequential()
    model.add(layers.Conv2D(64, (3, 3), padding='same', activation = 'relu', input_shape = datashape))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(64, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(128, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(128, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Dropout(0.4))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(256, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(256, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(256, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Dropout(0.4))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Dropout(0.4))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Conv2D(512, (3, 3), padding='same', activation = 'relu'))
    model.add(layers.Dropout(0.4))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation = 'relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(num_classes, activation = 'softmax'))
   
    if path != None:
        # Loads ImageNet pre-trained data
        model.load_weights(path)

    return model

def model_vgg19(datashape = (32, 32, 3), num_classes = 10, path = None):
    """
    VGG 19 Model for Keras

    Model Schema is based on 
    https://gist.github.com/baraldilorenzo/8d096f48a1be4a2d660d

    ImageNet Pretrained Weights 
    https://drive.google.com/file/d/0Bz7KyqmuGsilZ2RVeVhKY0FyRmc/view?usp=sharing

    Parameters:
      img_rows, img_cols - resolution of inputs
      channel - 1 for grayscale, 3 for color 
      num_classes - number of class labels for our classification task
    """
  
    model = Sequential()
    model.add(layers.ZeroPadding2D((1,1),input_shape = datashape))
    model.add(layers.Conv2D(64, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(64, 3, 3, activation='relu'))
    model.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(128, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(128, 3, 3, activation='relu'))
    model.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(256, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(256, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(256, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(256, 3, 3, activation='relu'))
    model.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.ZeroPadding2D((1,1)))
    model.add(layers.Conv2D(512, 3, 3, activation='relu'))
    model.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Add Fully Connected Layer
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1000, activation='softmax'))

    # Loads ImageNet pre-trained data
    model.load_weights('imagenet_models/vgg19_weights.h5')

    # Truncate and replace softmax layer for transfer learning
    model.layers.pop()
    model.outputs = [model.layers[-1].output]
    model.layers[-1].outbound_nodes = []
    model.add(layers.Dense(num_classes, activation='softmax'))

    return model

def model_vgg16_google(datashape = (32, 32, 3), num_classes = 10, path = None): 
    
    # img_rows, img_cols, channel=1, num_classes=None):
    """VGG 16 Model for Keras

    Model Schema is based on 
    https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3

    ImageNet Pretrained Weights 
    https://drive.google.com/file/d/0Bz7KyqmuGsilT0J5dmRCM0ROVHc/view?usp=sharing

    Parameters:
      img_rows, img_cols - resolution of inputs
      channel - 1 for grayscale, 3 for color 
      num_classes - number of categories for our classification task
    """

    model = Sequential()
    model.add(layers.ZeroPadding2D((1, 1), input_shape = datashape))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(512, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(512, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(512, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(512, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(512, (3, 3), activation='relu'))
    model.add(layers.ZeroPadding2D((1, 1)))
    model.add(layers.Conv2D(512, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=(2, 2)))

    # Add Fully Connected Layer
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1000, activation='softmax'))

    # Truncate and replace softmax layer for transfer learning
    model.layers.pop()
    model.outputs = [model.layers[-1].output]
    model.layers[-1].outbound_nodes = []
    model.add(layers.Dense(num_classes, activation='softmax'))

    # Uncomment below to set the first 10 layers to non-trainable (weights will not be updated)
    #for layer in model.layers[:10]:
    #    layer.trainable = False

    if path != None:
        # Loads ImageNet pre-trained data
        model.load_weights(path)

    return model


def apply_TopLayer(base_model, num_classes):
    
    # Build the dense Model 
    # incomming data format (4, 4, 512)
    
    model = models.Sequential() 
    model.add(base_model)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1000, activation='softmax'))

    # Truncate and replace softmax layer for transfer learning
    model.layers.pop()
    model.outputs = [model.layers[-1].output]
    model.layers[-1].outbound_nodes = []
    model.add(layers.Dense(num_classes, activation='softmax'))

    return model