import math
import random
import matplotlib.pyplot as plt

from mltools.annealing.animated_visualizer import animateTSP
from mltools.annealing.nodes_generator import Node_Generator
import numpy as np
import pandas as pd

class Simulated_Annealing():
    
    def __init__(self, nodes, config):
        ''' 
        animate the solution over time

        arguments:
        ----------
        coords        - array_like list of coordinates
        config        - configuration file 
        '''
        # Append default node (Wintrthur)
        nodes.append(0)

        # generate random list of nodes
        coords = Node_Generator(config['size_width'], config['size_height'], config['population_size']).generate()

        self.coords        = coords
        self.sample_size   = len(coords)
        self.temp          = config['temp']
        self.alpha         = config['alpha']
        self.stopping_temp = config['stopping_temp']
        self.stopping_iter = config['stopping_iter']
        self.iteration     = 1

        self.default_dist_matrix = pd.read_csv('data/sz_dist_matrix.csv', sep = ',')
        self.dist_mat            = self.vector_to_dist_matrix(nodes)
        # self.dist_mat.to_csv('/data/distance_matrix.csv')
        
        self.dist_matrix         = self.mat_conversion(self.dist_mat)
        self.curr_solution       = self.nearest_neighbour_solution_short(self.dist_matrix)
        self.porposed_route      = self.route(self.curr_solution, self.dist_mat)
        self.curr_distance       = self.weight(self.curr_solution)

        self.best_solution       = self.curr_solution
        self.solution_history    = [self.curr_solution]

        self.initial_distance    = self.curr_distance
        self.min_distance        = self.curr_distance

        self.weight_list         = [self.curr_distance]

        print('Intial distance: {} [m]'.format(self.curr_distance))

    def route(self, current_solution, dist_mat):

        solution = {}
        for i, idx in enumerate(current_solution):
            
            solution[idx] = dist_mat['cities'][idx]

        return solution

    def weight(self, sol):
        '''
        Calcuate weight
        '''
        weight = []

        for i, j in zip(sol, sol[1:] + [sol[0]]):
            
            weight.append(self.dist_matrix[i, j])

        return sum(weight)

    def acceptance_probability(self, candidate_weight):
        '''
        Acceptance probability as described in:
        https://stackoverflow.com/questions/19757551/basics-of-simulated-annealing-in-python
        '''
        return math.exp(-abs(candidate_weight - self.curr_distance) / self.temp)

    def accept(self, candidate):
        '''
        Accept with probability 1 if candidate solution is better than
        current solution, else accept with probability equal to the
        acceptance_probability()
        '''
        candidate_weight = self.weight(candidate)
        if candidate_weight < self.curr_distance:
            self.curr_weight = candidate_weight
            self.curr_solution = candidate
            if candidate_weight < self.min_distance:
                self.min_distance = candidate_weight
                self.best_solution = candidate

        else:
            if random.random() < self.acceptance_probability(candidate_weight):
                self.curr_distance = candidate_weight
                self.curr_solution = candidate

    def anneal(self):
        '''
        Annealing process with 2-opt
        described here: https://en.wikipedia.org/wiki/2-opt
        
        - Start with a random route
        - Perform a swap between two edges
        - Keep new route if it is shorter
        - Repeat (2-3) for all possible swaps
        - Repeat (1-5) for M possible initial configurations
        
        This algorithm is both faster, O(M*N^2) and produces better solutions. 
        The intuition behind the algorithm is that swapping two edges at a time untangles routes that cross over itself.
        '''
        while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
            candidate = list(self.curr_solution)
            l = random.randint(2, self.sample_size - 1)
            i = random.randint(0, self.sample_size - l)

            candidate[i: (i + l)] = reversed(candidate[i: (i + l)])

            self.accept(candidate)
            self.temp *= self.alpha
            self.iteration += 1
            self.weight_list.append(self.curr_distance)
            self.solution_history.append(self.curr_solution)

        print('Minimum distance: {} [m]'.format(self.min_distance))
        print('Improvement: {} [%]'.format(round((self.initial_distance - self.min_distance) / (self.initial_distance) * 100, 4)))

        return self.curr_solution

    def animateSolutions(self):
        animateTSP(self.solution_history, self.coords)

    def plotLearning(self):
        plt.plot([i for i in range(len(self.weight_list))], self.weight_list)
        line_init = plt.axhline(y=self.initial_weight, color='r', linestyle='--')
        line_min = plt.axhline(y=self.min_weight, color='g', linestyle='--')
        plt.legend([line_init, line_min], ['Initial weight', 'Optimized weight'])
        plt.ylabel('Weight')
        plt.xlabel('Iteration')
        plt.show()

    def vectorToDistMatrix(self, coords):
        '''
        Create the distance matrix
        '''
        return np.sqrt((np.square(coords[:, np.newaxis] - coords).sum(axis=2)))

    def vector_to_dist_matrix(self, nodes):

        # self.default_dist_matrix.iloc[:, 2:29]

        cities = self.default_dist_matrix['cities'][nodes]
        column_list = cities.to_list()
        column_list.append('cities')
        df_subset = self.default_dist_matrix[column_list]

        dist_matrix = df_subset[df_subset['cities'].isin(cities)] 
        sorted = self.rearrange(dist_matrix)
        sorted = ['cities'] + sorted

        dist_matrix = dist_matrix.reindex(columns=sorted)

        return dist_matrix

    def rearrange(self, dist_matrix):

        dist_mat = dist_matrix.copy()
        names = dist_mat['cities'].to_list()

        res = {}

        for i, key in enumerate(names):
            res[key] = dist_mat.index[dist_mat[key] == 0][0]
            
        return sorted(res, key=res.get)        

    def nearest_neighbour_solution_short(self, dist_matrix):
        '''
        Computes the initial solution (nearest neighbour strategy)
        '''
        node = 0 
        result = [node]

        nodes_to_visit = list(range(len(dist_matrix)))
        nodes_to_visit.remove(node)

        while nodes_to_visit:
            nearest_node = min([(dist_matrix[node][j], j) for j in nodes_to_visit], key=lambda x: x[0])
            node = nearest_node[1]
            nodes_to_visit.remove(node)
            result.append(node)

        return result

    def nearest_neighbour_solution(self, dist_matrix):

        nearest_node     = None
        node = last_node = 'Winterthur' 
        nodes_to_visit   = dist_matrix['cities'].to_list()
        result           = {'Winterthur': 0}

        while nodes_to_visit:
            if len(nodes_to_visit) != 1:
                nearest_node, dist = self.min_value(node, dist_matrix['cities'].to_list(), dist_matrix[node].to_list())
                result[nearest_node] = dist
                dist_matrix = self.clean_dist_matrix(dist_matrix, node)
                nodes_to_visit.remove(node)
                node = nearest_node
            else:
                result[last_node] = dist_matrix.iloc[0][last_node] 
                nodes_to_visit.remove(node)

        return result                

    def clean_dist_matrix(self, dist, node):
        dist.drop([node], axis = 1)
        dist = dist[dist['cities'] != node]

        return dist

    def min_value(self, master, name, dist):
        
        res = {} 
        for key in name: 
            for value in dist: 
                res[key] = value 
                dist.remove(value) 
                break
            
        res.pop(min(res, key=res.get))
        short_dist_name = min(res, key=res.get)
        return short_dist_name, res.get(short_dist_name)

    def mat_conversion(self, dist_mat):

        dist_mat.reset_index(drop=True, inplace=True)
        cities = dist_mat['cities']
        arr = []

        for i, name in enumerate(cities):
            values = dist_mat[dist_mat['cities'] == name]
            arr.append(values.iloc[0, 1:].tolist())

        arr = np.array(arr)
        return arr

    def get_dist_mat(self):
        return self.dist_mat


