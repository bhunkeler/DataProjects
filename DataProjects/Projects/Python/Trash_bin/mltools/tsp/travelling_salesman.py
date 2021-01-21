'''
Travelling salesman problem between cities.
'''

import pandas as pd
import random

class TSP():

    def __init__(self):
        pass

    def rearrange(self, dist_matrix):
        '''
        rearrange columns in distance matrix into a  identity matrix type. All zeros on the diagonal.

        arguments:
        ----------
        dist_matrix - containing distances between locations 

        return:
        -------
        sorted      - distance matrix 
        '''

        dist_mat = dist_matrix.copy()
        names = dist_mat['location'].to_list()

        res = {}

        for i, key in enumerate(names):
            res[key] = dist_mat.index[dist_mat[key] == 0][0]
                
        return sorted(res, key=res.get)   

    def vector_to_dist_matrix(self, dist_matrix, nodes, prod = True):
        '''
        create a distance matrix from a vector by just returning the requested nodes

        arguments:
        ----------
        dist_matrix - containing distances between locations
        nodes       - list of location points 

        return:
        -------
        dist_matrix - containing only columns and row of required nodes
        '''
        
        if prod == False:
            nodes = random.sample(range(1, 26), nodes)
        
        nodes = nodes + [0]

        locations = dist_matrix['location'][nodes]
        column_list = locations.to_list()
        column_list.append('location')
        df_subset = dist_matrix[column_list]

        dist_matrix = df_subset[df_subset['location'].isin(locations)] 
        sorted = self.rearrange(dist_matrix)
        sorted = ['location'] + sorted

        dist_matrix = dist_matrix.reindex(columns=sorted)

        return dist_matrix.iloc[:, :]

    def mat_conversion(self, dist_mat):
        '''
        Convert distance matrix into a dictionary 
        
        arguments:
        ----------
        dist_matrix - containing distances between locations 

        return:
        -------
        dictionary  - containing distances 
        '''
        
        dist_mat.reset_index(drop=True, inplace=True)
        locations = dist_mat['location']
        arr = []
        ref = {}

        for id, name in enumerate(locations):
            values = dist_mat[dist_mat['location'] == name]
            arr.append(values.iloc[0, 1:].tolist())
            ref[name] = id

        return arr, ref

    def create_data_model(self, default_dist_matrix, nodes, prod = True, num_vehicle = 1):
        '''
        Prepare the data.

        arguments:
        ----------
        nodes       - list of location points 

        return:
        -------
        data        - dictionary containing distance array
        ref         - reference between location and ID  
        '''
        data = {}

        if isinstance(default_dist_matrix, str):
            default_dist_matrix = pd.read_csv(default_dist_matrix, sep = ',')

        dist_mat = self.vector_to_dist_matrix(default_dist_matrix, nodes, prod)
        data['distance_matrix'], ref = self.mat_conversion(dist_mat)

        data['num_vehicles'] = num_vehicle
        data['depot'] = 0
        return data, ref

    def solution(self, manager, routing, solution):
        '''
        Prepare the final solution 

        arguments:
        ----------
        manager       - Routing Index Manager instance
        routing       - Routing Model of points   
        solution      - final solution 

        return:
        -------
        route           - list with ID's  
        route_distance  - list with min distance
        '''
        
        # print('Objective: {} [m]'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        route = []
        
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            route.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        route.append(manager.IndexToNode(index))
        plan_output += 'Route distance: {} [m]\n'.format(route_distance)
        
        return route, route_distance


    

