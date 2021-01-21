
import json
import pandas as pd
# from pandas.io.json import json_normalize 
from mltools.config import Configuration
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns

class TrashBin():

    def __init__(self, name = 'trash_bin'):

        map_config = Configuration('configs/trashbin.json')
        self._config = map_config._config

    def get_config(self, name):
        return self._config[name]

    def set_config(self, config):
        self._config = config

    def load_sensor_data(self, path):
        '''
        Load the sensor data from the json file 

        arguments:
        ----------
        path         - path to json file

        return:
        -------
        sensor data  - sensor data as a pandas data frame
        '''
       
        with open(path) as f:
            sensor_data = json.load(f)

        df_sensors = pd.json_normalize(sensor_data)
        df_sensors['level_50'] = np.where(df_sensors['filling_level'] >= 50, True, False)

        return df_sensors

    def update_sensor_data_sd(self, sensor_data, route):
        '''
        Update_sensor_data changes the update state to true if a trash bin
        has been emptied, but also resets the filling level to - 0 (empty)

        arguments:
        ----------
        sensor_data - received from server 
        nodes       - nodes which have been emptied (a node is a trashbin)

        return:
        -------
        sensor_data - maintained 

        '''
        origin = sensor_data.iloc[0]['city']

        for j, location in enumerate(route):
        
            if location != origin:
                id = sensor_data[sensor_data['city'] == location]['id']
                sensor_data.at[id, 'filling_level'] = 0
                sensor_data.at[id, 'maintenance']   = False
                sensor_data.at[id, 'update']        = True
                sensor_data.at[id, 'level_50']      = False

        sensor_data = sensor_data.drop(['level_50'], axis=1)

        return sensor_data

    def update_sensor_data(self, received_data, route, reference):
        '''
        Update_sensor_data changes the update state to true if a trash bin
        has been emptied, but also resets the filling level to - 0 (empty)

        arguments:
        ----------
        sensor_data - received from server 
        nodes       - nodes which have been emptied (a node is a trashbin)

        return:
        -------
        sensor_data - maintained 

        '''
        received_data = json.loads(received_data)
        origin = received_data[0]['city']

        for j, location in enumerate(route):
            
            if location != origin:
                id = int(reference[reference['city'] == location]['id'])
                received_data[id]['filling_level'] = 0
                received_data[id]['maintenance']   = False
                received_data[id]['update']        = True
                received_data[id]['level_50']      = False

        return received_data

    def preprocess_sensor_data(self, received_data):
        '''
        Preprocess sensor data from the json file 

        arguments:
        ----------
        received_data  - json data received from server

        return:
        -------
        sensor data  - sensor data as a pandas data frame
        '''

        sensor_data = json.loads(received_data )
        df_sensors = pd.json_normalize(sensor_data)
        df_sensors['level_50'] = np.where(df_sensors['filling_level'] >= 50, True, False)
        return df_sensors

    def plot_sensor_data_sns(self,sensor_data):
        '''
        plot the trash bin filling level of all trash bins and highlight the 
        ones which need to be consodered in the next upcomming route

        arguments:
        ----------
        sensor_data  - json data received from server

        return:
        -------
        plot
        '''

        blueish   = '#3891BC'
        redish    = '#E63323'
        yellowish = '#3891BC'

        plt.figure()
        plt.subplots(ncols=1, figsize=(10, 6)) 
        sns.set_style('darkgrid')
        conditional_colors = np.where(sensor_data['maintenance'] == True, 'y', np.where(sensor_data['filling_level'] >= 50, redish, blueish))
        # conditional_colors = np.where(sensor_data['filling_level'] >= 50, redish, blueish)

        sns.barplot(x = 'city', y = 'filling_level', data = sensor_data, palette = conditional_colors)
        plt.xlabel('locations', fontsize = 14)
        plt.ylabel('filling level', fontsize = 14)
        plt.title('Filling Level of Trash bins', fontsize = 18)
        plt.xticks(rotation=80)
        # plt.savefig('images/route.jpg')
        plt.show()        
        
