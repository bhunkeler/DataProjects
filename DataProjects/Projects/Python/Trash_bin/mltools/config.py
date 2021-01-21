import json
from bunch import Bunch
import os

class Configuration(object):
    _config = None
    _config_dict = None
    
    def __init__(self, json_file):

        '''
        Get the config from a json file
        
        arguments:
        ----------
        json_file
        
        return:
        -------
        config(namespace) or config(dictionary)
        '''
        # parse the configurations from the config json file provided
        with open(json_file, 'r') as config_file:
            self._config_dict = json.load(config_file)

        # convert the dictionary to a namespace using bunch lib
        self._config = Bunch(self._config_dict)
        
    def get_config(self):

        return self._config, self._config_dict

    def get_config_from_json(self, json_file):
        '''
        Get the config from a json file
        
        arguments:
        ----------
        json_file
        
        return:
        -------
        config(namespace) or config(dictionary)
        '''
        # parse the configurations from the config json file provided
        with open(json_file, 'r') as config_file:
            _config_dict = json.load(config_file)

        # convert the dictionary to a namespace using bunch lib
        _config = Bunch(_config_dict)

        return _config, _config_dict

    def process_config(self, config):
        
        config.summary_dir = os.path.join("../experiments", config.exp_name, "summary/")
        config.checkpoint_dir = os.path.join("../experiments", config.exp_name, "checkpoint/")
        return config

if __name__ == '__main__':
    config = Configuration('configs/hyperparameters.json')
    config, config_dict = config.get_config()
    config.process_config(config)
    end = 'end'
    

    