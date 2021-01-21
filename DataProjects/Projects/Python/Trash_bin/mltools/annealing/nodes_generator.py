import random
import numpy as np


class Node_Generator():
    
    def __init__(self, width, height, number_nodes):
        self._width = width
        self._height = height
        self._number_nodes = number_nodes

    def generate(self):
        xs = np.random.randint(self._width, size = self._number_nodes)
        ys = np.random.randint(self._height, size = self._number_nodes)

        return np.column_stack((xs, ys))

    def generate_nodes(self):
        
        nodes = random.sample(range(1, 26), self._number_nodes)

        return nodes
