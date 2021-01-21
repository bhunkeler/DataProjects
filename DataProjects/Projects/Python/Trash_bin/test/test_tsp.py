from mltools.tsp.route_analytics import Route_Analytics
from mltools.tsp.travelling_salesman import TSP

if __name__ == '__main__':

    tsp = TSP()
    data, ref = tsp.create_data_model('data/sz_dist_matrix.csv', 12, prod = False)

    route_analytics = Route_Analytics()
    manager, routing, solution = route_analytics.estimate_route(data)

    route, route_distance = tsp.solution(manager, routing, solution)

    print('Route Distance: {} [m]'.format(route_distance))
    print('Route IDs: {}'.format(route))
    route_locations = route_analytics.ref_map(route, ref)
    print(route_locations)
    end = 'end'