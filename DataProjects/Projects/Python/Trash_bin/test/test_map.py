from mltools.trash_bin import TrashBin
import ogr, osr
import gmaps.geojson_geometries
from mltools.map import Map
from mltools.location_map import Location_Map
import matplotlib.pyplot as plt

import googlemaps

if __name__ == "__main__":
    # print point in EPSG 4326
    tb = TrashBin()
    config = tb.get_config('trash_bin')
    map = Location_Map(config)
    
    zurich = map.city_point('Zurich')
    winterthur = map.city_point('Winterthur')
    Rychenberg = (47.50506485, 8.738057076445287)
    Stadthaus = (47.5004116, 8.7306033)

    distance_r_s, time_r_s = map.distance(Rychenberg, Stadthaus, mode = 'driving')
    distance_w_z, time_w_z = map.distance(winterthur, zurich, mode = 'driving')
    distance_b_s, time_b_s = map.distance(map.city_point('Bern'), map.city_point('Sion'), mode = 'driving')

    print('Driving Distance Rychenberg - Stadthaus: {0} [m] - travel duration: {1} [min]'.format(distance_r_s, time_r_s))
    print('Driving Distance Winterthur - Zürich: {0} [m] - travel duration: {1} [min]'.format(distance_w_z, time_w_z))
    print('Driving Distance Zürich - Sion: {0} [m] - travel duration: {1} [min]'.format(distance_b_s, time_b_s))

    # zurich = (47.369501, 8.538847)
    # bern   = (46.948384, 7.439946)
    # distance, duration = map.distance(zurich, bern)

    locations = []
    locations.append(winterthur)
    fig = map.plot_base_map('winterthur')

    fig = map.add_marker(fig, locations)


    end = 'end'
