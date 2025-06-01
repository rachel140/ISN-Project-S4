from shapely.geometry import Polygon, Point
import pandas as pd
import matplotlib.pyplot as plt


def create_polygon(fichier_csv):
    """
    Reads a csv file containing latitude and longitude coordinates,
    and returns a shapely polygon object built from those points.

    The csv is expected to have two columns: 'Latitude' and 'Longitude'.
    Each row represents one corner of the polygon, and the order of the
    rows determines how the polygon is drawn (i.e., the vertex order matters).

    Parameters:
        fichier_csv (str): Path to the CSV file with coordinate data.

    Returns:
        Polygon: A shapely polygon object created from the given coordinates.
    """
    # Load the CSV into a DataFrame; we assume it contains 'Latitude' and 'Longitude' columns
    df = pd.read_csv(fichier_csv, encoding='utf-8', delimiter=",")
    
    coords = []  # This list will store all the coordinate pairs (longitude, latitude)

    # Go through each row in the CSV file to extract the coordinates
    for (_, row) in df.iterrows():
        lat = row['Latitude']  # Get the latitude value from the row
        lon = row['Longitude']  # Get the longitude value from the row
        
        # Shapely expects coordinates in (x, y) format → that's (lon, lat) for geographic data
        coords.append((lon, lat))  # Add the coordinate pair to the list

    # Once all points are collected, we create a polygon object using Shapely
    polygon = Polygon(coords)

    # Return the polygon so we can use it later (e.g. for plotting or geometry checks)
    return polygon

# Specify the name of the CSV file containing the corner points of the polygon
file = 'carre_coord.csv'

# Call the function to build the polygon from the CSV
polygon1 = create_polygon(file)

# Use matplotlib to plot the outline of the polygon
# .exterior gives the outer boundary, .xy returns the x and y coordinate arrays
plt.plot(*polygon1.exterior.xy)

# Show the plot in a window
plt.show()
