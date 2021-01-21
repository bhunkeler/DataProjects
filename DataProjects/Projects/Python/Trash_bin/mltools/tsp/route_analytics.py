from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class Route_Analytics():

    def __init__(self):
        pass 

    def estimate_route(self, data):
        '''
        Estimate the best solution 

        arguments:
        ----------
        data     - distance dictionary

        return:
        -------
        manager       - Routing Index Manager instance
        routing       - Routing Model of points   
        solution      - final solution 
        '''

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            
            # Returns the distance between the two nodes.
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        return manager, routing, solution

    def ref_map(self, route, ref):
        '''

        arguments:
        ----------
        route     - estimated route
        ref       - reference dictionary ID's to points resp. locations

        return:
        -------
        solution  - list of points to approach
        '''
        solution = []
        for i, idx in enumerate(route):
            solution.append(self.map_id_to_key(ref, idx))

        return solution

    def map_id_to_key(self, ref, id):
        '''
        map id to reference (location names)
        
        arguments:
        ----------
        ref       - reference dictionary ID's to points resp. locations
        id        - id's of final solution 

        return:
        -------
        key       - location name
        '''
        for key, value in ref.items():
            if id == value:
                return key