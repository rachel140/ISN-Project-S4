import netCDF4 as nc
from shapely.geometry import Polygon, Point, MultiPoint
import pandas as pd
from math import cos, radians

class ElevationData:

    def __init__(self, world_map, country_map, contour_map,):

       self.netcdf_files  = world_map
       self.contour_map = contour_map
       self.country_map = country_map
       
       self.elevation_dict = {} # Initialize an empty dictionary: { elevation → [[lat, lon], ...] }
       self.polygon = None
       #self.dict_test = {50: [[-80, 90], [65.234114, 100.368612]], 49: [[-80, 90], [65.234114, 100.368612]], 899: [[-80, 90], [65.234114, 100.368612]], -1000: [[-80, 90], [65.234114, 100.368612]]}
       #self.dict_test = dict(list(self.elevation_dict.items())[5:])
       
       #methods
       self.create_polygon(self.contour_map)
       self.create_elevation()
       self.climate_features = {'drought_index': 1.0,'flood_risk': 1.0, 'heatwave_days': 10, 'wildfire_risk': 1.0}
       self.nb_refugees = self.compute_refugees(2030,50,0.21)
       #print(self.nb_refugees)            
            
    def create_elevation(self):
        
        """
        Load the data from several nc files containing the elevation, longitude and altitude of all points on Earth (with a precision to the 15 arc-minute). Convert the data to create a dictionary with the key being an elevation and the value a list of tuples (latitude, longitude), in degrees, of all points being at the given elevation (in meters).

        elevation_dico = { “elevation1” : [ [lat1, long1], [lat2, long2], …],
                          evation2” : [ [lat1, long1], [lat2, long2], …],...}
                          
        Parameters: 
            -------
            files_name: list of strings 
            corresponding to the name of the nc files containing the data for the latitude, longitude and elevation of all points on Earth.

        Returns:
            -------
            elevation_dico: dict
            associates each elevation in meters to a list of tuples (latitude, longitude) in degrees at the given elevation.
        """

        

        # Read the NetCDF file
        with nc.Dataset(self.netcdf_files, mode='r') as dataset:
            # Read the latitude and longitude arrays of the NetCDF file
            lats = dataset.variables['lat'][:]
            lons = dataset.variables['lon'][:]

            # Read the elevation matrix (2D array: lat x lon)
            elevations = dataset.variables['z'][:]

            
            # Define the step of the array to have a 5° resolution
            # Convert the 60 arc-minute resolution :
            # Given that 1°= 60 arc-minute, 5° = 300 arc-mintues
            # So keep every 5nd point
            step = 5

            # Get indices that will give us data at 0.5° spacing
            lat_indices = list(range(0, len(lats), step))
            lon_indices = list(range(0, len(lons), step))

            # Loop through selected lat/lon lists
            for i in lat_indices:
                for j in lon_indices:
                    lat = round(float(lats[i]))
                    lon = round(float(lons[j]))
                    elev = round(float(elevations[i, j]))  

                    # Initialize list for this elevation if it doesn't exist
                    if elev not in self.elevation_dict:
                        self.elevation_dict[elev] = []

                        # Add the coordinate pair [lat, lon] to the elevation_dict dictionary at index elevation (elev)
                        self.elevation_dict[elev].append([lat, lon])

            
    
    def create_polygon(self, csv_file):
        """
        Load a CSV file with coordinates and create a polygon shape from it.
        The CSV has columns 'latitude' and 'longitude'.
        
        Parameters
        ----------
        fichier_csv : str
            The path to the CSV file that contains the boundary coordinates.
    
        Returns
        -------
        polygon : shapely.geometry.Polygon
            The polygon created from the coordinates.
        """
        # read the CSV file with the coordinates
        df = pd.read_csv(csv_file, encoding='utf-8', delimiter=",")
        coords = []
    
        # loop through each row to extract lat/lon and store them as (lon, lat)
        for (_, row) in df.iterrows():
            lat = row['Latitude']
            lon = row['Longitude']
            coords.append((lon, lat))  # shapely expects (x=lon, y=lat)
    
        # create the polygon from all the points
        self.polygon = Polygon(coords)
        return self.polygon
            
    def test_if_point_in(self, where_clicked):
        """
        Test if a clicked point is inside the polygon.
        The polygon should already be created before calling this function.
    
        Parameters
        ----------
        where_clicked : tuple
            Coordinates of the point clicked (lat, lon)
    
        Returns
        -------
        is_inside : bool
            True if the point is inside the polygon, False otherwise
        """
        # extract lat/lon from the clicked point
        lat, lon = where_clicked
    
        # create a shapely point using lon/lat
        point = Point(lon, lat)
    
        # check if the point is inside the polygon we created
        is_inside = self.polygon.contains(point)
    
        return is_inside

                
            
    def build_dico_per_long(self, sea_level):
        """
        Reads a CSV file of France mainland elevation points and creates a dictionary
        where each key is a longitude (rounded to 1 decimal) and the value is the average
        elevation above sea level at that longitude (only if it's above sea level).
    
        Parameters
        ----------
        sea_level : float
            The reference sea level we want to compare elevation to.
    
        Returns
        -------
        dico_per_long : dict
            Dictionary of the form {longitude_rounded : avg_elevation_above_sea_level}
            Only includes longitudes where the average elevation is above the sea level.
        """
        coordinates = pd.read_csv(self.country_map, encoding='utf-8', delimiter=",")

        # round longitude to 1 decimal place
        coordinates['longitude'] = coordinates['longitude'].round(1)

        # compute average elevation per longitude
        grouped = coordinates.groupby('longitude')['elevation'].mean()

        # filter based on the sea level
        dico_per_long = {}
        for lon, avg_elev in grouped.items():
            if avg_elev > sea_level:
                adjusted_elev = round(avg_elev - sea_level)
                dico_per_long[lon] = adjusted_elev

        return dico_per_long
    
        
    def compute_refugees(self, year, elevation_year, elevation_2022):
        """
        Compute the number of climatic refugees due to the elevation of sea level.
        Define the limits of the continents considering the points the most at north, east, south and west of each continent.
        store these limits in lists of tuples (lat, long) in order north, east, south and west:
            limits_continent= [(lat_max_north, long_max_north),(lat_max_east, long_max_east),(lat_max_south, long_max_south),(lat_max_west, long_max_west)]
    
        Returns:
        -------
            nb_refugees: (int) number of climatic refugees according to the year chosen by the user and the scenario.
        """
        nb_refugees = 32000000   #initialize the number of climatic refugees to 32 million in 2022
        one_deg_lat = 111.320   #conversion of one degree in latitude into a distance in kilometers
        one_deg_long = 111.320  #conversion of one degree in longitude into a distance in kilometers
    
    
        # # Define the base average inhabitant density for each continent in number of inhabitants per squared kilometer in 2022
        base_density = {'asia': 149.7,'africa': 47.2,'america': 33.7,'europe': 109.0,'oceania': 5.2}

        # Annual population growth rates per continent 
        growth_rate = {'asia': 0.006,'africa': 0.025,'america': 0.007,'europe': 0.003, 'oceania': 0.012}

        # Calculate how many years have passed since 2022 (no negative years)
        years_since_2022 = max(0, year - 2022)
        # If the user puts a year too far in the future (like 3000), we limit it to 500 years
        # to avoid unrealistic density due to the exponential growth 
        if year - 2022 > 500:
            years_since_2022 = 500
    
        # Compute projected population densities
        density_asia = base_density['asia'] * (1 + growth_rate['asia']) ** years_since_2022
        density_africa = base_density['africa'] * (1 + growth_rate['africa']) ** years_since_2022
        density_america = base_density['america'] * (1 + growth_rate['america']) ** years_since_2022
        density_europe = base_density['europe'] * (1 + growth_rate['europe']) ** years_since_2022
        density_oceania = base_density['oceania'] * (1 + growth_rate['oceania']) ** years_since_2022
    
    
        # Define the limits of each continent and create polygons with these limits
        limits_asia = [[30.0, 80.0], [180.0, 80.0], [180.0, -15.0], [130.0, -15.0], [90.0, -20.0], [50.0, -20.0], [30.0, 0.0], [20.0, 10.0], [20.0, 40.0], [30.0, 80.0]]
        polygon_asia = MultiPoint(limits_asia).convex_hull  # Create the polygon that approximates Asia's shape
    
        limits_africa = [[-30.0, 40.0], [60.0, 40.0], [60.0, -40.0], [20.0, -50.0], [-30.0, -40.0], [-30.0, 0.0], [-30.0, 40.0]]
        polygon_africa = MultiPoint(limits_africa).convex_hull
    
        limits_namerica = [[-170.0, 85.0], [-30.0, 85.0], [-30.0, 10.0], [-60.0, 5.0], [-100.0, 5.0], [-170.0, 10.0], [-170.0, 85.0]]
        polygon_namerica = MultiPoint(limits_namerica).convex_hull
    
        limits_samerica = [-90.0, 15.0], [-30.0, 15.0], [-30.0, -60.0], [-90.0, -60.0], [-90.0, 15.0]
        polygon_samerica = MultiPoint(limits_samerica).convex_hull
    
        limits_europe = [-30.0, 75.0], [60.0, 75.0], [60.0, 35.0], [30.0, 30.0], [0.0, 30.0], [-30.0, 40.0], [-30.0, 75.0]
        polygon_europe = MultiPoint(limits_europe).convex_hull
    
        limits_oceania = [[110.0, 0.0], [180.0, 0.0], [180.0, -50.0], [110.0, -50.0], [110.0, 0.0]]
        polygon_oceania = MultiPoint(limits_oceania).convex_hull
        
        # Approximate surface affected by one point 
        surface = 5 * one_deg_lat * 5 * one_deg_long
        
        if year > 2022:  # Check if the user chose a year in the future
            for elev, list_points in self.elevation_dict.items():
    
                # Loop through all elevation levels between the 2022 level and the level in the chosen future year
                if elev < elevation_year and elev >= elevation_2022:
                    for coord in list_points: 
                        point = Point(coord[1], coord[0])  # Create a point with longitude first (x), then latitude (y)
                        
                        # Check which continent the point belongs to and compute number of refugees
                        if polygon_asia.contains(point):
                            # Add number of refugees based on population density and affected area
                            nb_refugees += density_asia * surface
                            
                        elif polygon_africa.contains(point):
                            nb_refugees += density_africa * surface
                            
                        elif polygon_namerica.contains(point):                            
                            nb_refugees += density_america * surface
                            
                        elif polygon_samerica.contains(point):                            
                            nb_refugees += density_america * surface
                            
                        elif polygon_europe.contains(point):                            
                            nb_refugees += density_europe * surface
                            
                        elif polygon_oceania.contains(point):                            
                            nb_refugees += density_oceania * surface
                            
            other_refugees = self.estimate_other_climatic_refugees(year)
            nb_refugees += other_refugees
        
        if nb_refugees > 1000000000:
            nb_refugees = round(nb_refugees / 1000000000, 3)
            refugees = f'{nb_refugees} billion'
            
        elif nb_refugees > 1000000:
            nb_refugees = round(nb_refugees / 1000000, 3)
            refugees = f'{nb_refugees} million'
            
        return refugees  # Return the total number of estimated refugees
    

                    
    def estimate_other_climatic_refugees(self, year):
        """
        Estimate number of climatic refugees due to the climatic events other than sea level rise.
    
        Parameters
        ----------
        year : int
            The year chosen by the user for prediction.
    
        Returns
        -------
        refugees : int
            Estimated number of additional climatic refugees based on the evolution of key climate features.
        """
    
        # compute the number of years since 2022 and limit it to 500 to avoid unrealistic projections
        years_passed = max(0, min(500, year - 2022))
    
        # compute the value of each climate feature based on its base value and the annual growth
        drought = round(self.climate_features.get('drought_index', 0) + 0.0175 * years_passed, 2)  # increase drought index
        flood = round(self.climate_features.get('flood_risk', 0) + 0.017 * years_passed, 2)      # increase flood risk
        heat = int(self.climate_features.get('heatwave_days', 0) + 0.8 * years_passed)           # increase number of heatwave days
        wildfire = round(self.climate_features.get('wildfire_risk', 0) + 0.0175 * years_passed, 2)  # increase wildfire risk
    
        # estimate the number of refugees caused by each event
        refugees = (drought * 10000000) + (flood * 35000000) + (heat * 2000000) + (wildfire * 3000000)
    
        # return the total number of additional climatic refugees due to these events
        return int(refugees)
                            
                            
                            
    ##____Old version to color the map of the world according to the sea level using dictionary_____                        
    # def color_map(self, canvas, width, height):
    #     """
    #     Color the  map based on the sea level. 
    #     If the elevation is greater than the water level, then the colour is green.
    #     If the elevation is smaller than the water level, then the colour is blue.

    #     Parameters:
    #         ----------
    #         elevation_dico : dict
    #              Dictionary containing the elevation as key and the    associated coordinates (longitudes and latitudes) as values.
    #              year : int
    #              Considered year for observing the elevation

    #     Returns:
    #         -------
    #         None.
    #     """
    #     # Clear existing drawings
    #     canvas.delete("all")

    #     elevation = self.controller.get_sea_level(year)
    #     for elev, liste in self.elevation_dict.items():
            
    #         #Check if the points in the dictionary elevation_dict are below or above sea level
            
    #         if elev < elevation:  #If the elevation is below sea level
    #             for lat, long in liste:
    #                 x,y = width * lat, height * long  #Convert the lat, long into coordinates adapted to the canva
    #                 canvas.create_circle(x-1, y-1, x+1, y+1, fill="blue", width=2)  # Color each point at a given elevation below sea level in blue
                    
    #         else:     #If the elevation is above sea level
    #             for lat, long in liste: 
    #                 x,y = width * lat, height * long   #Convert the lat, long into coordinates adapted to the canva
    #                 canvas.create_circle(x-1, y-1, x+1, y+1, fill="green", width=2) # Color each point at a given elevation above sea level in green
                    
        
