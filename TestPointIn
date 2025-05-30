from shapely.geometry import Polygon, Point
import pandas as pd
import matplotlib.pyplot as plt

def create_polygon(fichier_csv):
            df = pd.read_csv(fichier_csv, encoding='utf-8', delimiter=",")
            coords = []
            for (_, row) in df.iterrows():
                lat = row['Latitude']
                lon = row['Longitude']
                coords.append((lon, lat))
            #print(len(coords))
            polygon = Polygon(coords)
            return polygon
        

def test_if_point_in(where_clicked, polygon):
            lat, lon = where_clicked
            point = Point(lon, lat)
            is_inside = polygon.contains(point)
            return is_inside
        
def test_function():        
    file = 'carre_coord.csv'
    polygon1 = create_polygon(file)
    plt.plot(*polygon1.exterior.xy)
    plt.show()
    
    cases = [
        # Points inside
        ((5.0, 5.0), True),
        ((2.3, 9), True),
        ((6, 2), True),

        # Points not in that polygon
        ((-80.0, 4.0), False),
        ((5.0, 20.0), False),
        ((-120.0, -35.0), False),

        # Borders coordinates
        ((10.0, 2.0), False),  
        ((3.0, 10.0), False),  
        ((10.0, 10.0), False),  
        
    ]

    # Loop through each test point and check if the point is correctly placed
    test = True
    for ((x, y), expected) in cases:
        point = Point(x, y)
        result = polygon1.contains(point)
        if result != expected : 
            print(f"Test failed for point ({x}, {y}). Expected {expected}, got {result}.")
            test = False
    if test : 
        print("All points passed.")

test_function()
