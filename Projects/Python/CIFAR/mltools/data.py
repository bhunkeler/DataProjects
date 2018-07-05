
class DataStore:
    
    '''
    Reference:

    [1] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. 
    arXiv preprint arXiv:1409.1556, 2014. https://arxiv.org/pdf/1409.1556.pdf
    '''
    # Constructor
    def __init__(self, x_train, y_train, x_test, y_test, x_val, y_val ):
        self.__x_train  = x_train
        self.__y_train  = y_train
        self.__x_val    = x_val
        self.__y_val    = y_val 
        self.__x_test   = x_test
        self.__y_test   = y_test 


    def getTrainData(self):
        
        return self.__x_train, self.__y_train

    def getTestData(self):
            
        return self.__x_test, self.__y_test

    def getValidationData(self):
            
        return self.__x_val, self.__y_val

    def getAllData(self):
            
        return self.__x_train, self.__y_train, self.__x_test, self.__y_test, self.__x_val, self.__y_val

    def setTrainData(self, x_train, y_train):
        
        self.__x_train = x_train
        self.__y_train = y_train

    def setTestData(self, x_test, y_test):
        
        self.__x_test = x_test
        self.__y_test = y_test

    def setValidationData(self, x_val, y_val):
        self.__x_val = x_val
        self.__y_val = y_val

    def setAllData(self, x_train, y_train, x_test, y_test, x_val, y_val):

        self.__x_train = x_train 
        self.__y_train = y_train 
        self.__x_test  = x_test
        self.__y_test  = y_test 
        self.__x_val   = x_val
        self.__y_val   = y_val
