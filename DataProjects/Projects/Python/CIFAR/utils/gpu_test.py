import numpy as np
import tensorflow as tf
import datetime
import os


deviceGPU0 = '/gpu:0'
deviceGPU1 = '/gpu:1'
deviceCPU0 = '/cpu:0'
deviceGPU_ = '/device:GPU:0'

#num of multiplications to perform
n = 100

# Create random large matrix
matrix_size = 1e3

def test_1():
    # Creates a graph.
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    c = tf.matmul(a, b)
    # Creates a session with log_device_placement set to True.
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    # Runs the op.
    print(sess.run(c))

def test_2(device= '/cpu:0'):
    
    with tf.Session() as sess:
     with tf.device(device):
         with tf.Session() as sess:
             with tf.device(device):
                matrix1 = tf.constant([[3., 3.]])
                matrix2 = tf.constant([[2.],[2.]])
                product = tf.matmul(matrix1, matrix2)
                result = sess.             matrix1 = tf.constant([[3., 3.]])
                matrix2 = tf.constant([[2.],[2.]])
                product = tf.matmul(matrix1, matrix2)
                result = sess.run(product)
                print(result)

def main():
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"]=""

    # from numba import cuda 
    # from numba import *
    from tensorflow.python.client import device_lib
    print(device_lib.list_local_devices())

    test_1()
    test_2(deviceGPU0)
    # test_3(deviceGPU0)
    test_2(deviceGPU1)

def test_3(device):
    A = np.random.rand(matrix_size, matrix_size).astype('float32')
    B = np.random.rand(matrix_size, matrix_size).astype('float32')

    # Creates a graph to store results
    c1 = []
    with tf.device(device):
       a = tf.constant(A)
       b = tf.constant(B)
       #compute A^n and B^n and store results in c1
       c1.append(matpow(a, n))
       c1.append(matpow(b, n))

       sum = tf.add_n(c1)

    t1 = datetime.datetime.now()
    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
        # Runs the op.
        sess.run(sum)
        t2 = datetime.datetime.now()

    print("computation time: " + str(t2-t1))

# Define matrix power
def matpow(M, n):
    if n < 1: #Abstract cases where n < 1
        return M
    else:
        return tf.matmul(M, matpow(M, n-1))

if __name__ == '__main__':
    main()

