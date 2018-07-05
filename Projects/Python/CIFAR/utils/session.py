class session:
    
    '''
    
    '''

    def __init__(self, config ):

        self.__config = config
        self.__model = object()

    def get_config(self):
        return self.__config

    def set_config(self, config):
        self.__config = config

    def get_model(self):
        return self.__model

    def set_model(self, model):
        self.__model = model
