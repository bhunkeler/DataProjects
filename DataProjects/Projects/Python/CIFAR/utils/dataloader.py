import pandas as pd
import pickle
import os
import numpy as np

import keras
from keras.datasets import mnist, cifar10
from keras.utils import to_categorical

from urllib.request import urlretrieve
import tarfile
import zipfile
import sys


def load_mnist_data(image_size, validation = True, show = True):
    
    '''
    load mnist data from keras dataset. Reshape the images and normalize to values
    between 0..1. Convert labels to categorical values.

    Attributes:
    image_size - size of images
    validation - extract a validation set
    show       - show the size of each item (training, test and validation data)

    return train_images, train_labels, test_images, test_labels
    '''

    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    m_train = len(train_images)
    m_test  = len(test_images)
    # print('Training data: {}'.format(m_train))
    # print('Test data: {}'.format(m_test)) 

    train_images = train_images.reshape((m_train, image_size, image_size, 1))
    train_images = train_images.astype('float32') / 255
    test_images  = test_images.reshape((m_test, image_size, image_size, 1))  
    test_images  = test_images.astype('float32') / 255

    train_labels = to_categorical(train_labels)
    test_labels  = to_categorical(test_labels)

    if validation:
        # extract a validation set from the training data 
        validation_images = train_images[50000:60000]
        validation_labels = train_labels[50000:60000]

        train_images = train_images[:50000]
        train_labels = train_labels[:50000]
    else:
        validation_images = None
        validation_labels = None

    if show:
        if validation:
            print('Training data: {}'.format(train_images.shape))
            print('Training labels: {}'.format(train_labels.shape))
            print('Test data: {}'.format(test_images.shape))
            print('Test labels: {}'.format(test_labels.shape))
            print('Validation data: {}'.format(validation_images.shape))
            print('Validation labels: {}'.format(validation_labels.shape))
        else:
            print('Training data: {}'.format(train_images.shape))
            print('Training labels: {}'.format(train_labels.shape))
            print('Test data: {}'.format(test_images.shape))
            print('Test labels: {}'.format(test_labels.shape))
           

    return train_images, train_labels, test_images, test_labels, validation_images, validation_labels

def Cifar10_DataPreparation(num_classes, validation = True):
       (x_train, y_train), (x_test, y_test) = cifar10.load_data()
       
       x_val = x_train[40000:50000]
       y_val = y_train[40000:50000]
       x_train = x_train[:40000]
       y_train = y_train[:40000]
        
       print('Train data {}'.format(x_train.shape))
       print('Test data {}'.format(x_test.shape))
       print('Val data {}'.format(x_val.shape))
            
       # Convert class vectors to binary class matrices.
       y_train = to_categorical(y_train, num_classes)
       y_test  = to_categorical(y_test, num_classes)
       y_val  = to_categorical(y_val, num_classes)
   
       # convert values beween 0..1
       x_train = x_train.astype('float32') / 255
       x_test  = x_test.astype('float32') / 255
       x_val   = x_val.astype('float32') / 255

       return x_train, y_train, x_test, y_test, x_val, y_val


    
def load_cifar10_data(data_dir):
    '''Return train_data, train_labels, test_data, test_labels
       The shape of data is 32 x 32 x3
    '''
    train_data = None
    train_labels = []

    for i in range(1, 6):
        data_dic = unpickle(os.path.join(data_dir, "data_batch_{}".format(i)))
        if i == 1:
            train_data = data_dic['data']
        else:
            train_data = np.vstack((train_data, data_dic['data']))
        train_labels += data_dic['labels']

    test_data_dic = unpickle(data_dir + "/test_batch")
    test_data = test_data_dic['data']
    test_labels = test_data_dic['labels']

    train_data = train_data.reshape((len(train_data), 3, 32, 32))
    train_data = np.rollaxis(train_data, 1, 4)
    train_labels = np.array(train_labels)

    test_data = test_data.reshape((len(test_data), 3, 32, 32))
    test_data = np.rollaxis(test_data, 1, 4)
    test_labels = np.array(test_labels)

    return train_data, train_labels, test_data, test_labels

    
def _load_batch(path, file):
    
    path = os.path.join(path, file)

    # f = open(path, 'rb')
    dict = pd.read_pickle(path)
    # dict = cPickle.load(f)
    images = dict['data']
    #images = np.reshape(images, (10000, 3, 32, 32))
    labels = dict['labels']
    imagearray = np.array(images)   #   (10000, 3072)
    labelarray = np.array(labels)   #   (10000,)
    
    return imagearray, labelarray

    
   
def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
         dict = pickle.load(fo, encoding='bytes')
    return dict

def get_data_set(name="train", cifar=10):
    x = None
    y = None
    l = None

    # cwd = os.getcwd()
    # cp = os.path.dirname(os.path.abspath(__file__))
    # maybe_download_and_extract()

    folder_name = "cifar_10" if cifar == 10 else "cifar_100"

    meta_path  = './data/' + folder_name + '/cifar-10-batches-py/batches.meta'
    batch_path = './data/' + folder_name + '/cifar-10-batches-py/data_batch_'
    test_path  = './data/' + folder_name + '/cifar-10-batches-py/test_batch'
     
    try: 
        f = open(meta_path, 'rb')
        
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except: 
        print("Unexpected error:", sys.exc_info()[0])
    # raise

    datadict = pickle.load(f, encoding='latin1')
    f.close()
    l = datadict['label_names']

    if name is "train":
        for i in range(5):
            f = open(batch_path + str(i + 1), 'rb')
            datadict = pickle.load(f, encoding='latin1')
            f.close()

            _X = datadict["data"]
            _Y = datadict['labels']

            _X = np.array(_X, dtype=float) / 255.0
            _X = _X.reshape([-1, 3, 32, 32])
            _X = _X.transpose([0, 2, 3, 1])
            _X = _X.reshape(-1, 32*32*3)

            if x is None:
                x = _X
                y = _Y
            else:
                x = np.concatenate((x, _X), axis=0)
                y = np.concatenate((y, _Y), axis=0)

    elif name is "test":
        f = open(test_path, 'rb')
        datadict = pickle.load(f, encoding='latin1')
        f.close()

        x = datadict["data"]
        y = np.array(datadict['labels'])

        x = np.array(x, dtype=float) / 255.0
        x = x.reshape([-1, 3, 32, 32])
        x = x.transpose([0, 2, 3, 1])
        x = x.reshape(-1, 32*32*3)

    def dense_to_one_hot(labels_dense, num_classes=10):
        num_labels = labels_dense.shape[0]
        index_offset = np.arange(num_labels) * num_classes
        labels_one_hot = np.zeros((num_labels, num_classes))
        labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1

        return labels_one_hot

    return x, dense_to_one_hot(y), l

def _print_download_progress(count, block_size, total_size):
    pct_complete = float(count * block_size) / total_size
    msg = "\r- Download progress: {0:.1%}".format(pct_complete)
    sys.stdout.write(msg)
    sys.stdout.flush()

def maybe_download_and_extract(url, main_directory):
    # main_directory = "./data_set/"
    cifar_10_directory = "cifar_10/"

    # cwd = os.getcwd()

    if not os.path.exists(main_directory):
        os.makedirs(main_directory)

        # url = "http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
        filename = url.split('/')[-1]
        file_path = os.path.join(main_directory, filename)
        zip_cifar_10 = file_path
        file_path, _ = urlretrieve(url=url, filename=file_path, reporthook=_print_download_progress)

        print()
        print("Download finished. Extracting files.")
        if file_path.endswith(".zip"):
            zipfile.ZipFile(file=file_path, mode="r").extractall(main_directory)
        elif file_path.endswith((".tar.gz", ".tgz")):
            tarfile.open(name=file_path, mode="r:gz").extractall(main_directory)
        print("Done.")

        os.rename(main_directory+"./cifar-10-batches-py", cifar_10_directory)
        os.remove(zip_cifar_10)