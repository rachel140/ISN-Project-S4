from shapely.geometry import Point, MultiPoint

def test_create_limits_countries():
    """
    

    Returns
    -------
    None.

    """
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
    
    
    # Define test points with expected results
    # Each tuple: ((long, lat), polygon, expected_result)
    test_cases = [
        # Normal valid points (inside)
        ((100.0, 40.0), polygon_asia, True),
        ((-1.5, 12.3), polygon_africa, True),
        ((-99.1, 19.4), polygon_namerica, True),
        ((-58.4, -34.6), polygon_samerica, True),
        ((10.0, 50.0), polygon_europe, True),
        ((151.2, -33.9), polygon_oceania, True),

        # Valid Earth points, but not in that polygon
        ((-80.0, 0.0), polygon_asia, False),
        ((120.0, 30.0), polygon_africa, False),
        ((-120.0, -35.0), polygon_namerica, False),
        ((40.0, 60.0), polygon_samerica, False),
        ((150.0, -30.0), polygon_europe, False),
        ((30.0, 60.0), polygon_oceania, False),

        # Impossible Earth coordinates (longitude and latitude outside valid range)
        ((200.0, 50.0), polygon_asia, False),   # Invalid longitude
        ((-190.0, -10.0), polygon_africa, False),  # Invalid longitude
        ((40.0, 100.0), polygon_europe, False),  # Invalid latitude
        ((0.0, -100.0), polygon_samerica, False),  # Invalid latitude
        ((300.0, 300.0), polygon_namerica, False),  # Invalid longitude and latitude
        ((-999.0, -999.0), polygon_oceania, False),  # Invalid longitude and latitude
    ]

    # Loop through each test point and check if the point is correctly placed
    test = True
    for ((lon, lat), polygon, expected) in test_cases:
        point = Point(lon, lat)
        result = polygon.contains(point)
        if result != expected : 
            print(f"Test failed for point ({lon}, {lat}). Expected {expected}, got {result}.")
            test = False
    if test : 
        print("All continent polygon tests passed successfully.")
        
test_create_limits_countries()
