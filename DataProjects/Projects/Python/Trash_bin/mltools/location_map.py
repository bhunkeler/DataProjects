from googlemaps.convert import latlng
from mltools.trash_bin import TrashBin
import ogr, osr
import gmaps
# import gmaps.datasets
# import gmaps.geojson_geometries
import googlemaps
import pandas as pd
import random
import datetime


class Location_Map():

    # def __init__(self, config, path):
    #     self._config      = config
    #     self._locations   = pd.read_csv(path, sep = ',')
    #     self._key         = config['api_key']
    #     self._google_maps = googlemaps.Client(key = self._key)
    #     self._gmaps       = None
        
    #     self._inputEPSG = 2056
    #     self._outputEPSG = 4326

    #     # create a geometry from coordinates
    #     self._point = ogr.Geometry(ogr.wkbPoint)

    #     inSpatialRef = osr.SpatialReference()
    #     inSpatialRef.ImportFromEPSG(self._inputEPSG)

    #     outSpatialRef = osr.SpatialReference()
    #     outSpatialRef.ImportFromEPSG(self._outputEPSG)

    #     self._coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    #     pass
    
    def __init__(self, config, location_data):
        self._config      = config

        if isinstance(location_data, str):
            self._locations   = pd.read_csv(location_data, sep = ',')
        else:
            self._locations   = location_data
        
        self._key         = config['api_key']
        self._google_maps = googlemaps.Client(key = self._key)
        self._gmaps       = None
        
        self._inputEPSG = 2056
        self._outputEPSG = 4326

        # create a geometry from coordinates
        self._point = ogr.Geometry(ogr.wkbPoint)

        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(self._inputEPSG)

        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(self._outputEPSG)

        self._coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

        pass

    def get_gmaps(self):
        return self._gmaps

    def set_gmaps(self, gmaps):
        self._gmaps = gmaps

    def convert_cartesian_to_lat_Ion(self, pointX, pointY):
        '''
        Convert cartesian coordinates to latitude and longitude (decimal) 

        arguments:
        ----------
        pointX - cartesian point X coordinate
        pointY - cartesian point Y coordinate

        return:
        -------
        pointX - latitude decimal
        pointY - longitude decimal
        '''

        # create a geometry from coordinates
        self._point.AddPoint(pointX, pointY)

        # transform point
        self._point.Transform(self._coordTransform)

        return round(self._point.GetX(), 6), round(self._point.GetY(), 6)    

    def plot_base_map(self, place = 'switzerland'):
        '''
        Create base map of switzerland

        arguments:
        ----------
        none 

        return:
        -------
        fig - gmaps figure 
        '''
        figure_layout = {
            'width': '1600px',
            'height': '1100px',
            'border': '1px solid black',
            'padding': '1px'
        }

        if place == 'switzerland':
            center_coords = self._config['switzerland_ctr']
        else: 
            center_coords = self._config['winterthur_ctr']
        
        gmaps.configure(api_key= self._config['api_key'])
        fig = gmaps.figure(layout=figure_layout, center = center_coords, zoom_level = 9)

        return fig

    def add_marker(self, fig, locations):
        '''
        Add a 'list' of markers to the map 

        arguments:
        ----------
        fig       - figure object
        locations - list of locations 

        return:
        -------
        fig       - enriched figure object 
        '''
        
        marker_layer = gmaps.marker_layer(locations)
        fig.add_layer(marker_layer)
        
        return fig

    def add_direction(self, fig, origin, destination, mode = 'DRIVING'):
        '''
        Add direction to the map 

        arguments:
        ----------
        fig         - figure object
        origin      - starting point
        destination - end point

        return:
        -------
        fig         - enriched figure object 
        '''
        stroke_color   = 'red',
        stroke_opacity = 1.0  
        stroke_weight  = 2.0

        color_palette = ['#eb4034', '#4a9932', '#3b8796', '#4e64cf', '#a14bcc', '#ab203c']
        color = random.choice(color_palette)
        
        direction = gmaps.directions_layer(origin, 
                                           destination, 
                                           stroke_color = color, 
                                           stroke_opacity = stroke_opacity, 
                                           stroke_weight = stroke_weight, 
                                           travel_mode = 'DRIVING')
        fig.add_layer(direction)
        return fig

    def distance(self, origin, destination, mode = 'driving'):
        '''
        Calculates the distance between origin (lat, lon) and destination (lat, lon)

        arguments:
        ----------
        origin     - (lat, lon) - zurich = (47.369501, 8.538847) 
        desination - (lat, lon) - bern   = (46.948384, 7.439946)
        mode       - wlaking, driving, bicycling 

        return:
        -------
        distance - distance in meters
        duration - duration in minutes
        '''

        distance = self._google_maps.distance_matrix(origin, destination, mode=mode)
        distance_m = distance["rows"][0]["elements"][0]["distance"]["value"]
        duration_sec = distance["rows"][0]["elements"][0]["duration"]["value"]

        return distance_m, round((duration_sec / 60), 2)

    def preprocess_cantons(self):
        '''
        prepare cities data file and store as csv
        '''
        city = ['Winterthur','Zurich', 'Bern', 'Luzern', 'Altdorf', 'Schwyz', 'Sarnen', 'Stans', 'Glarus', 'Zug', 'Fribourg', 'Solothurn', 'Basel', 'Liestal', 'Schaffhausen', 'Herisau', 'Appenzell', 'St_Gallen', 'Chur', 'Aarau', 'Frauenfeld', 'Bellinzona', 'Lausanne', 'Sion', 'Neuchatel', 'Geneve', 'Delemont']

        coord = [
        [2696846.000, 1262447.000], [2683100.000, 1247100.000], [2600100.000, 1199700.000], [2665841.000, 1211943.000], [2691800.000, 1192900.000], 
        [2692400.000, 1208500.000], [2661400.000, 1194200.000], [2670600.000, 1201100.000], [2723440.000, 1211300.000], [2681943.000, 1224632.000], 
        [2577900.000, 1183600.000], [2606900.000, 1228800.000], [2611300.000, 1267600.000], [2622300.000, 1259400.000], [2689600.000, 1283800.000], 
        [2738700.000, 1250300.000], [2748684.000, 1244215.000], [2746200.000, 1254600.000], [2759300.000, 1191000.000], [2645800.000, 1249000.000], 
        [2709600.000, 1268400.000], [2722400.000, 1116800.000], [2538200.000, 1152400.000], [2594000.000, 1120100.000], [2561240.000, 1204880.000], 
        [2500000.000, 1117900.000], [2593000.000, 1245900.000]]

        point = [
            (47.505637,8.724139), (47.369501,8.538847),(46.948384,7.439946),(47.055245,8.305225),(46.880884,8.643002),(47.021109,8.654043),(46.896079,8.24438),(46.957229,8.36617),
            (47.041239,9.062997),(47.167576,8.519434),(46.803191,7.149124),(47.210102,7.529706),(47.559017,7.58876),(47.484987,7.734502),(47.698682,8.632284),(47.388917,9.275753),
            (47.332025,9.40592),(47.425957,9.37646),(46.851053,9.527574),(47.390236,8.045227),(47.557165,8.894863),(46.191535,9.024186),(46.520039,6.633279),(46.232315,7.360869),
            (46.993842,6.929066),(46.205108,6.142976),(47.363905,7.34596)]

        df = pd.DataFrame()
        df['city'] = city
        df['coordinates'] = coord
        df['lat'] = None
        df['lon'] = None
        df['point'] = point

        for i in range(len(df)):
            lat, lon = self.convert_cartesian_to_lat_Ion(df['coordinates'].iloc[i][0], df['coordinates'].iloc[i][1])
            df['lat'].iloc[i] = lat
            df['lon'].iloc[i] = lon

        df.to_csv('data/cities.csv')

    def city_coord(self, city = 'Winterthur'):
        '''
        Retrieve coordinates lat, lon of a city

        arguments:
        ----------
        city       - name of the city

        return:
        -------
        coordinates - location coordinates
        '''
        coord = (self._cities[self._cities['city'] == city].lat, self._cities[self._cities['city'] == city].lon)

        return coord
    
    def location_lat_lon(self, location = 'Winterthur'):
        '''
        Retrieve coordinates lat, lon of a city

        arguments:
        ----------
        city       - name of the city

        return:
        -------
        lat        - latitude
        lon        - longitude
        '''
        lat = self._locations[self._locations['location'] == location].lat.values
        lon = self._locations[self._locations['location'] == location].lon.values

        return lat[0], lon[0]

    def location_point(self, location = 'Winterthur'):
        '''
        Retrieve coordinates lat, lon of a city

        arguments:
        ----------
        location       - name of the city

        return:
        -------
        point - location point
        '''
        lat = self._locations[self._locations['location'] == location].lat.values
        lon = self._locations[self._locations['location'] == location].lon.values

        return (lat[0], lon[0])

    def distance_matrix(self, file_name):
        
        location_names = self._locations['location']
        dist_matrix = pd.DataFrame()
        dist_matrix['location'] = location_names

        for i, target_name in enumerate(location_names):
            
            target_point = self.location_point(target_name) 
            dist = []
            
            for i, location_name in enumerate(location_names):
                
                dest_point = self.location_point(location_name)
                distance, time = self.distance(target_point, dest_point)
                dist.append(distance)
            
            dist_matrix[target_name] = dist

        dt = datetime.datetime.now().strftime("%d.%m.%y-%H_%M")
        dist_mat = 'data/' + file_name + '_' + dt + '.csv'

        dist_matrix.to_csv(dist_mat)





