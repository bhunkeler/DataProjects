from mltools.annealing.nodes_generator import Node_Generator
from mltools.annealing.simulated_annealing import Simulated_Annealing
import pandas as pd

from mltools.trash_bin import TrashBin
from mltools.map import Map

def main():

    tb = TrashBin()
    map = Map(tb.get_config('trash_bin'))
    config = tb.get_config('tsp')

    # generate random list of nodes
    coords = Node_Generator(config['size_width'], config['size_height'], config['population_size']).generate()
    nodes = Node_Generator(config['size_width'], config['size_height'], 5).generate_nodes()
    
    # Append default node (Wintrthur)
    nodes.append(0)

    # run simulated annealing algorithm with 2-opt 
    sa = Simulated_Annealing(coords, nodes, config)
    curr_solution = sa.anneal()

    route = sa.route(curr_solution, sa.get_dist_mat())

    for i, city in enumerate(route):
        print(city)

    # animate
    # sa.animateSolutions()

    # show the improvement over time
    # sa.plotLearning()

    end = 'end'


if __name__ == "__main__":
    main()
