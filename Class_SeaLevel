import csv

class SeaLevel:
    def __init__(self):
        self.dico_sea_level_past = {}
        self.load_data_sea_level("Sea_level_rise.csv")

    def load_data_sea_level(self, file_sea_level, delimiteur = ';', jump_first_line = True):
	"""
	Load the data from a file containing the average sea level on Earth for all past years since 2015. Convert them into a dictionary dico_sea_level where each key corresponds to a year and the associated value corresponds to the average sea elevation.  
	
	Parameters:
	----------
	file_sea_level: str 
	name of the csv file containing the data for the sea level elevation for the past 10 years
	Returns: 
	----------
	dico_sea_level: dict 
	associating each year to the average sea level 
	"""

        dico_sea_level_past = {}
        with open(file_sea_level, 'r', encoding = 'utf-8') as our_data:
            csvReader = csv.reader(our_data, delimiter = delimiteur)
            if jump_first_line:
                next(csvReader)
            for row in csvReader:
                if int(row[0]) % 5 == 0:   #Keep only the values every five years
                    self.dico_sea_level_past[int(row[0])]= float(row[1])
       
        return self.dico_sea_level_past



    def compute_sea_level_1(self, year):
	"""
	Compute the average sea level elevation for a given year (int) in the future using the model prediction from the GIEC scenario 1.
	
	Parameter:
	----------
	year: int 
	above 2025 corresponding to a year in the future at which we want to compute the sea level according to the predictions
	Returns:
	----------
	sea_level:  float 
	value of the average sea level elevation for the given year 
	"""

        return round(6*(10**(-82))*year**24.366,3)

    def compute_sea_level_2(self, year):
	"""
	Compute the average sea level elevation for a given year (int) in the future using the model prediction from the GIEC scenario 2.
	
	Parameter:
	----------
	year: int 
	above 2025 corresponding to a year in the future at which we want to compute the sea level according to the predictions
	Returns:
	----------
	sea_level:  float 
	value of the average sea level elevation for the given year 
	"""

        return round(7*(10**(-91))*year**27.078,3)

    def compute_sea_level_3(self, year):
	"""
	Compute the average sea level elevation for a given year (int) in the future using the model prediction from the GIEC scenario 3.
	
	Parameter:
	----------
	year: int 
	above 2025 corresponding to a year in the future at which we want to compute the sea level according to the predictions
	Returns:
	----------
	sea_level:  float 
	value of the average sea level elevation for the given year 
	"""

        return round(1*(10**(-107))*year**32.127,3)

    def compute_sea_level_4(self, year):
	"""
	Compute the average sea level elevation for a given year (int) in the future using the model prediction from the GIEC scenario 4.
	
	Parameter:
	----------
	year: int 
	above 2025 corresponding to a year in the future at which we want to compute the sea level according to the predictions
	Returns:
	----------
	sea_level:  float 
	value of the average sea level elevation for the given year 
	"""

        return round(3*(10**(-128))*year**38.388,3)

    def retrieve_sea_level(self, year, scenario):
	"""
	Retrieve the sea level for a year given as a parameter. If the value of the sea level is already in the dictionary dico_sea_level, no computation is needed. If the value of the given year is not in dico_sea_level, compute the sea level  using the function compute_sea_level and store it in dico_sea_level at the index year.
		
	Parameters:
	----------
	year: int 
	year at which we want to retrieve the sea level
	scenario: int
	GIEC scenario choosen by the user
	
	Returns: 
	----------
	sea_level : float 
	value of the sea level elevation for the given year
	"""

        if year in self.dico_sea_level_past.keys():
            sea_level = self.dico_sea_level[year]
       
        elif scenario == 1:
            sea_level = self.compute_sea_level_1(year)
            
        elif scenario == 2:
            sea_level = self.compute_sea_level_2(year)
            
        elif scenario == 3:
            sea_level = self.compute_sea_level_3(year)
            
        elif scenario == 4:
            sea_level = self.compute_sea_level_4(year)
            

        return sea_level
