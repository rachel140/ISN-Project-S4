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
        
file = 'carre_coord.csv'
polygon1 = create_polygon(file)
plt.plot(*polygon1.exterior.xy)
plt.show()
