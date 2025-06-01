from shapely.geometry import Polygon, Point
import pandas as pd
import matplotlib.pyplot as plt


def create_polygon(fichier_csv):
    """
    Reads a csv file with 'latitude' and 'longitude' columns and creates a polygon.

    The csv file should contain coordinates that represent the vertices of a polygon.
    The order of the points in the CSV determines the polygon’s shape.

    Parameters:
        fichier_csv (str): The path to the csv file containing coordinate data.

    Returns:
        Polygon: A shapely polygon object constructed from the coordinates.
    """
    # Read the csv file into a DataFrame using comma as delimiter
    df = pd.read_csv(fichier_csv, encoding='utf-8', delimiter=",")

    coords = []  # Initialize an empty list to store polygon vertices

    # Iterate over each row in the DataFrame to extract latitude and longitude
    for (_, row) in df.iterrows():
        lat = row['Latitude']  # Latitude is the north-south position (y-axis)
        lon = row['Longitude']  # Longitude is the east-west position (x-axis)

        # Append each point as a tuple (lon, lat) because Shapely expects (x, y) format
        coords.append((lon, lat))

    # Create a polygon from the list of coordinates
    polygon = Polygon(coords)

    # Return the polygon object so it can be used later
    return polygon


def test_if_point_in(where_clicked, polygon):
    """
    Tests if a given point lies inside a given polygon.

    Parameters:
        where_clicked (tuple): A tuple (latitude, longitude) representing the point to test.
        polygon (polygon): A shapely polygon object.

    Returns:
        is_inside (bool): True if the point is inside the polygon, False otherwise.
    """
    # Unpack the input point (lat, lon)
    lat, lon = where_clicked

    # Create a Shapely Point object with coordinates (lon, lat)
    point = Point(lon, lat)

    # Use the polygon’s 'contains' method to check if the point lies inside
    is_inside = polygon.contains(point)

    return is_inside


def test_function():
    """
    Runs tests on the polygon creation and point-in-polygon functionality.

    - Loads a polygon from a csv file.
    - Plots the polygon boundary using matplotlib.
    - Tests multiple points to check if they lie inside or outside the polygon.
    - Prints the test results.
    """
    # Define the path to the csv file containing the polygon vertices
    file = 'carre_coord.csv'

    # Create the polygon by reading coordinates from the csv file
    polygon1 = create_polygon(file)

    # Plot the polygon border by extracting the exterior boundary's coordinates
    plt.plot(*polygon1.exterior.xy)
    plt.show()

    # Define a list of test cases with points and expected results (inside or outside the polygon)
    cases = [
        # Points expected to be inside the polygon
        ((5.0, 5.0), True),
        ((2.3, 9), True),
        ((6, 2), True),

        # Points expected to be outside the polygon
        ((-80.0, 4.0), False),
        ((5.0, 20.0), False),
        ((-120.0, -35.0), False),

        # Points on the polygon's border (considered outside for the contains() function)
        ((10.0, 2.0), False),
        ((3.0, 10.0), False),
        ((10.0, 10.0), False)]
    

    # Initialize a variable to verify the validity of the test
    test = True

    # Loop through each test case
    for ((x, y), expected) in cases:
        point = Point(x, y)  # Create a point from the test coordinates

        # Check if the polygon contains the point (True or False)
        result = polygon1.contains(point)

        # If the result doesn’t match the expected value, print an error message
        if result != expected:
            print(f"Test failed for point ({x}, {y}). Expected {expected}, got {result}.")
            test = False  # Mark the test as failed

    # After all tests, print a success message all points have passed
    if test:
        print("All points passed.")


# Run the test function
test_function()
