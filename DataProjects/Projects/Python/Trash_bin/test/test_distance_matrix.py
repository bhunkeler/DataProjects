import numpy as np
import pandas as pd

from mltools.location_map import Location_Map
from mltools.trash_bin import TrashBin


def wt_location_dist_mat():
    
    tb = TrashBin()
    config = tb.get_config('trash_bin')
    location_data = pd.read_csv('data/wt_locations.csv', sep = ',')
    location_data.columns = ['id', 'location', 'lat', 'lon', 'point']

    l_map = Location_Map(config, 'data/wt_locations.csv')
    l_map.distance_matrix('wt_dist_mat')

def sz_location_dist_mat():
    
    tb = TrashBin()
    config = tb.get_config('trash_bin')
    location_data = pd.read_csv('data/sz_locations.csv', sep = ',')
    location_data.columns = ['id', 'location', 'lat', 'lon', 'point']

    l_map = Location_Map(config, 'data/sz_locations.csv')
    l_map.distance_matrix('sz_dist_mat')

if __name__ == "__main__":

    wt_location_dist_mat()
    sz_location_dist_mat()

    end = 'end'

    


    
    



