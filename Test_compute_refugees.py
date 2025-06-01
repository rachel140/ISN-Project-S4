from shapely.geometry import MultiPoint, Point


def compute_refugees(list_points, year=2030, elevation_year=1.21, elevation_2022=0.21):
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
    growth_rate = {'asia': 0.005,'africa': 0.025,'america': 0.007,'europe': 0.000, 'oceania': 0.012}

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

    if year > 2022:  # Check if the user chose a year in the future
        for coord in list_points:         
            point = Point(coord[1], coord[0])  # Create a point with longitude first (x), then latitude (y)
            
            # Approximate surface affected by one point (flat Earth assumption for simplicity)
            surface = one_deg_lat * one_deg_long
            
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
                        
        other_refugees = estimate_other_climatic_refugees(year)
        nb_refugees += other_refugees

    return int(nb_refugees)  # Return the total number of estimated refugees

def estimate_other_climatic_refugees(year):
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
    # Define default climate features
    climate_features = {
        'drought_index': 1.0,
        'flood_risk': 1.0,
        'heatwave_days': 10,
        'wildfire_risk': 1.0}
    # compute the number of years since 2022 and limit it to 500 to avoid unrealistic projections
    years_passed = max(0, min(500, year - 2022))

    # compute the value of each climate feature based on its base value and the annual growth
    drought = round(climate_features.get('drought_index', 0) + 0.0175 * years_passed, 2)  # increase drought index
    flood = round(climate_features.get('flood_risk', 0) + 0.017 * years_passed, 2)      # increase flood risk
    heat = int(climate_features.get('heatwave_days', 0) + 0.8 * years_passed)           # increase number of heatwave days
    wildfire = round(climate_features.get('wildfire_risk', 0) + 0.0175 * years_passed, 2)  # increase wildfire risk

    # estimate the number of refugees caused by each event
    refugees = (drought * 10000000) + (flood * 35000000) + (heat * 2000000) + (wildfire * 3000000)

    # return the total number of additional climatic refugees due to these events
    return int(refugees)
                        

def test_refugees_all_asia():
    """
    Test that adding points all located in Asia increases the number of climatic refugees.
    We check that the number exceeds the 2022 baseline when a year in the future is used.
    """
    points = [[40, 100], [45, 110], [35, 120]]  # Coordinates within Asia
    result = compute_refugees(points, year=2035, elevation_year=1.5, elevation_2022=0.21)
    if result > 32000000:
        print("test_refugees_all_asia passed")  # Expect increase due to the added exposure in Asia
    else:
        print("test_refugees_all_asia failed")

def test_refugees_all_ocean():
    """
    Test that when all points are located in oceanic areas (outside any polygon),
    the number of refugees remains the same as the base case (no additional exposure).
    """
    points = [[0, -150], [-30, -120], [0, -100]]  # All points are in the Pacific Ocean
    result = compute_refugees(points, year=2035, elevation_year=1.5, elevation_2022=0.21)
    base = compute_refugees([], year=2035, elevation_year=1.5, elevation_2022=0.21)
    if result == base:
        print("test_refugees_all_ocean passed")  # Expect no change compared to an empty input
    else:
        print("test_refugees_all_ocean failed")

def test_refugees_multiple_continents():
    """
    Test that including points across several continents correctly increases the refugee estimate.
    Each point should contribute based on the corresponding continent's density.
    """
    points = [[40, 100], [0, 20], [50, -10], [-10, 140]]  # Asia, Africa, Europe, Oceania
    result = compute_refugees(points, year=2040, elevation_year=1.8, elevation_2022=0.21)
    if result > 32000000:
        print("test_refugees_multiple_continents passed")  # Expect increased estimate
    else:
        print("test_refugees_multiple_continents failed")

def test_no_points_base_case():
    """
    Test the base case where no coordinates are provided.
    Should return the initial refugee count for 2022 with no elevation impact.
    """
    result = compute_refugees([], year=2022, elevation_year=0.21, elevation_2022=0.21)
    if result == 32000000:
        print("test_no_points_base_case passed")  # Baseline test with no exposure
    else:
        print("test_no_points_base_case failed")

def test_max_year():
    """
    Test that refugee projection is limited at 500 years in the future.
    Running the function compute_refugees for the year 2522 and 3022 should lead to the same result.
    """
    result_500 = compute_refugees([], year=2522, elevation_year=10.0, elevation_2022=0.21)
    result_1000 = compute_refugees([], year=3022, elevation_year=15.0, elevation_2022=0.21)
    if result_500 == result_1000:
        print("test_max_year passed")  # Year limit successfully enforced
    else:
        print("test_max_year failed")

def test_climatic_refugees_estimation():
    """
    Test the accuracy of the estimate_other_climatic_refugees function.
    Verifies that the formula matches the expected refugee count for the given year.
    """
    year = 2030
    result = estimate_other_climatic_refugees(year)

    # Manually compute expected refugee count
    years = 2030 - 2022
    expected = (
        round(1.0 + 0.01 * years, 2) * 50000 +
        round(1.0 + 0.015 * years, 2) * 100000 +
        int(10 + 0.8 * years) * 20000 +
        round(1.0 + 0.012 * years, 2) * 75000
    )

    if result == int(expected):
        print("test_climatic_refugees_estimation passed")  # Match expected output
    else:
        print("test_climatic_refugees_estimation failed")

def test_refugees_increasing_with_area():
    """
    Test that increasing the number of flooded points increases the total refugee estimate.
    This checks the linearity of the exposure model.
    """
    point = [40, 100]  # Asia
    result_small = compute_refugees([point], year=2035, elevation_year=1.5, elevation_2022=0.21)
    result_large = compute_refugees([point] * 10, year=2035, elevation_year=1.5, elevation_2022=0.21)
    if result_large > result_small:
        print("test_refugees_increasing_with_area passed")  # More area should imply more refugees
    else:
        print("test_refugees_increasing_with_area failed")

    



# Run all tests
test_refugees_all_asia()
test_refugees_all_ocean()
test_refugees_multiple_continents()
test_no_points_base_case()
test_max_year()
test_climatic_refugees_estimation()
test_refugees_increasing_with_area()
