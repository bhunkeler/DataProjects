
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
from matplotlib.textpath import TextToPath
import tilemapbase
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

import seaborn as sns
import shapely.speedups
shapely.speedups.enable()

from mltools.trash_bin import TrashBin

import gmaps
import gmaps.datasets
import gmaps.geojson_geometries
import json
import googlemaps.distance_matrix
from mltools.map import Map



def london():
    import gmaps
    import gmaps.datasets

    london_congestion_zone_path = gmaps.datasets.load_dataset('london_congestion_zone')
    london_congestion_zone_path[:2]

    fig = gmaps.figure(center=(51.5, -0.1), zoom_level=12)
    london_congestion_zone_polygon = gmaps.Polygon(london_congestion_zone_path,stroke_color='blue',fill_color='blue')
    drawing = gmaps.drawing_layer(features=[london_congestion_zone_polygon],show_controls=False)
    fig.add_layer(drawing)
    fig

def swiss():
    # read country borders
    swiss_geo_path        = gpd.read_file('data/2019_THK_PRO/PRO/01_INST/Gesamtfläche_gf/K4_suis18480101_gf/K4suis18480101gf_ch2007Poly.shp')
    country_geo_path      = gpd.read_file('data/swiss_geodata/gg20/ggg_2020-LV95/shp/g2k20.shp')
    
    # read cantonal borders
    canton_geo_path       = gpd.read_file('data/2019_THK_PRO/PRO/01_INST/Gesamtfläche_gf/K4_kant19970101_gf/K4kant19970101zg_ch2007Pnts.shp') 

    # read lage data
    lake_large_geo_path   = gpd.read_file('data/2019_THK_PRO/PRO/00_TOPO/K4_seenyyyymmdd/k4seenyyyymmdd11_ch2007Poly.shp') 
    lake_small_geo_path   = gpd.read_file('data/2019_THK_PRO/PRO/00_TOPO/K4_seenyyyymmdd/k4seenyyyymmdd22_ch2007Poly.shp') 
    
    # read city coordinates
    ct_cap_city_geo_path  = gpd.read_file('data/2019_THK_PRO/PRO/00_TOPO/K4_stkt19970101/k4stkt19970101kk_ch2007Pnts.shp')

def geneva2zurich():

    geneva = (46.2, 6.1)
    montreux = (46.4, 6.9)
    zurich = (47.4, 8.5)
    fig = gmaps.figure()
    geneva2zurich = gmaps.directions_layer(geneva, zurich)
    
    return geneva, zurich, geneva2zurich

def markers_direction():
    figure_layout = {
        'width': '1600px',
        'height': '1100px',
        'border': '1px solid black',
        'padding': '1px'
        }

    switzerland_ctr_coord = config['switzerland_ctr']
    gmaps.configure(api_key= config['api_key'])
    fig = gmaps.figure(layout=figure_layout, center = switzerland_ctr_coord, zoom_level = 9)

    winterthur_lat, winterthur_lon = map.city_lat_lon('Winterthur')
    zurich_lat, zurich_lon = map.city_lat_lon('Zurich')
    winterthur_point = map.city_point('Winterthur')
    zurich_point = map.city_point('Zurich')

    locations = [(winterthur_lat, winterthur_lon), (zurich_lat, zurich_lon)]
    fig = map.add_marker(fig, locations)
    fig = map.add_direction(fig, winterthur_point, zurich_point, mode = 'DRIVING')


def distance_matrix():
    
    zurich = map.city_coord('Zurich')
    winterthur = map.city_coord('Winterthur')

    distance, time = map.distance(winterthur, zurich, mode = 'driving')
    distance, time = map.distance(map.city_coord('Bern'), map.city_coord('Sion'), mode = 'driving')



if __name__ == "__main__":
    
    tb = TrashBin()
    config = tb.get_config('trash_bin')
    map = Map(config)

    cities = pd.read_csv('data/cities.csv', sep = ',')

    city_names = cities['city']
    dist_matrix = pd.DataFrame()
    dist_matrix['cities'] = city_names

    for i, target_name in enumerate(city_names):
        
        target_point = map.city_point(target_name) 
        dist = []
        
        for i, city_name in enumerate(city_names):
            
            dest_point = map.city_point(city_name)
            distance, time = map.distance(target_point, dest_point)
            dist.append(distance)
            pass
        
        dist_matrix[target_name] = dist
        pass

    dist_matrix.to_csv('data/dist_matrix.csv')

    end = 'end'

