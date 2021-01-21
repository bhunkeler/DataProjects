
from IPython import get_ipython

import numpy as np
import pandas as pd

# Trash_bin main
from mltools.trash_bin import TrashBin

# Maps
from mltools.location_map import Location_Map

# Simulated annealing
from mltools.annealing.nodes_generator import Node_Generator
from mltools.annealing.simulated_annealing import Simulated_Annealing

# Route analytis
from mltools.tsp.route_analytics import Route_Analytics 
from mltools.tsp.travelling_salesman import TSP
from mltools.streaming.tcp_client import TCP_Client

import json

def tsp(nodes, path):
    
    prod = True
    tsp = TSP()
    if prod:
        nodes = nodes 
    else:
        nodes = 12
    data, ref = tsp.create_data_model(path, nodes, prod = True)

    route_analytics = Route_Analytics()
    manager, routing, solution = route_analytics.estimate_route(data)
    route, route_distance = tsp.solution(manager, routing, solution)
    route_tsp = route_analytics.ref_map(route, ref)

    print('Route Distance: {} [m]'.format(route_distance))
    print('Route IDs: {}'.format(route))
    print(route_tsp)
    return route_tsp

def sa():
    # Simulated Annealing
    # ------------------------------------------

    nodes = Node_Generator(config['size_width'], config['size_height'], 5).generate_nodes()
    sa = Simulated_Annealing(nodes, config) # run simulated annealing algorithm with 2-opt 
    solution = sa.anneal()

    route = sa.route(solution, sa.get_dist_mat())
    print(route)
    return route

def get_markers(route):
    location_markers = []

    for location in route: 
        location_markers.append(map.location_point(location))
    
    return location_markers

if __name__ == '__main__':

    host = '192.168.0.151'
    port = 65432

    country = False
    
    if country:
        location_data = 'data/sz_locations.csv'
        dist_matrix   = 'data/sz_dist_matrix.csv'
        sensor_data   = 'data/sz_sensor.json'
    else:
        location_data = 'data/wt_locations.csv'
        dist_matrix   = 'data/wt_dist_matrix.csv'
        sensor_data   = 'data/wt_sensor.json'

    # Dummy data load remove latter on 
    # sensor_data = 'data/sz_sensor.json'

    # Initialize TCP Connection 
    # ------------------------------------------
    
    client = TCP_Client(host, port, request_type = 'init') 
    client.initialize(sensor_data)
    client = None

    tb = TrashBin()
    map = Location_Map(tb.get_config('trash_bin'), location_data)
    config = tb.get_config('tsp')

    # Trash_bin sensor data
    # ------------------------------------------

    client = TCP_Client(host, port, request_type = 'init') 
    received_data = client.request_sensor_data()
    client = None
    sensor_data = tb.preprocess_sensor_data(received_data)

    # sensor_data = tb.load_sensor_data(sensor_data)

    sensors = np.where(sensor_data['filling_level'] >= 50)
    maintenance = np.where(sensor_data['maintenance'] == True)
    nodes = set(np.concatenate([sensors[0], maintenance[0]]))
    nodes = list(nodes)  # convert to list again

    # Markers TSP / SA
    # ------------------------------------------
    route_tsp = tsp(nodes, dist_matrix) # TSP
    location_markers_tsp = get_markers(route_tsp)
    print(location_markers_tsp)

    # Markers TSP / SA
    # ------------------------------------------

    # route_sa  = sa()  # Simulated Annealing
    # location_markers_sa = get_markers(list(route_sa.values()))
    # print(location_markers_sa)

    # Map
    # ------------------------------------------

    fig = map.plot_base_map()
    print(route_tsp) 

    fig = map.add_marker(fig, location_markers_tsp)

    length = len(route_tsp)
    for i, location in enumerate(location_markers_tsp):
        if i < (length - 1):
            fig = map.add_direction(fig, location, location_markers_tsp[i + 1])

    fig

    # --------
    def update_sensor_data(received_data, route, reference):

        received_data = json.loads(received_data)
        origin = received_data[0]['city']
        

        for j, location in enumerate(route):
            
            if location != origin:
                id = int(reference[reference['city'] == location]['id'])
                received_data[id]['filling_level'] = 0
                received_data[id]['maintenance']   = False
                received_data[id]['update']        = True
                received_data[id]['level_50']      = False
                

    # --------    

    reference = sensor_data[['id', 'city']]
    sensor_data = tb.update_sensor_data(received_data, route_tsp, reference)

    client = TCP_Client(host, port, request_type = 'init') 
    received_data = client.update_sensor_data(sensor_data)



