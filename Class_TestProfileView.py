import customtkinter as ctk
import pandas as pd
import os
from Class_ProfileView import ProfileView


class TestProfileView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Profile View Test")
        self.geometry("1000x700")

        # This frame is like a container where all other GUI elements will be
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create an instance of the ProfileView class that will draw the elevation graph
        self.profile_view = ProfileView()

        # Try to load and prepare elevation data from the .csv
        self.dico_per_long = self.build_dico_per_long()

        # If the dictionary isn't empty, it means we loaded the data
        if self.dico_per_long:
            self.profile_view.draw_profile(
                self.frame,
                width=800,
                height=500,
                dico_per_long=self.dico_per_long,
                sea_level=0.2 )  # sea level in meters
            
        else:
            # If something went wrong during the data loading, show an error message in the GUI
            error_label = ctk.CTkLabel(self.frame, text="Error: No elevation data loaded.")
            error_label.pack(pady=20)

    def build_dico_per_long(self):
        fichier_csv = 'fr_mainland_only.csv'

        # Step 1: Make sure the csv file actually exists before we try to read it
        # Without this check, the program would bug if the file is missing
        if not os.path.exists(fichier_csv):
            print(f"CSV file not found: {fichier_csv}")
            return {}

        # Step 2: Load the csv using pandas
        # We are assuming the file has the columns 'Longitude' and 'Elevation'
        coordinates = pd.read_csv(fichier_csv, encoding='utf-8', delimiter=",")

        # Step 3: Check if the expected columns are present in the data
        # If the column names are wrong or missing, the next steps would not work
        expected_columns = {'Longitude', 'Elevation'}
        if not expected_columns.issubset(coordinates.columns):
            print("Error: CSV file must contain 'Longitude' and 'Elevation' columns.")
            return {}

        # Step 4: Round the longitude values to 1 decimal place
        # This groups nearby coordinates together so the profile graph looks smoother
        coordinates['Longitude'] = coordinates['Longitude'].round(1)

        # Step 5: Group the data by the rounded longitude values
        # For each group (i.e. each longitude), calculate the average elevation
        # This gives us one elevation value per longitude to plot
        grouped = coordinates.groupby('Longitude')['Elevation'].mean()

        # Step 6: Convert the grouped data into a dictionary
        # This makes it easier to pass into the drawing function later
        dico_per_long = {lon: round(avg_elev) for lon, avg_elev in grouped.items()}

        # Now we return the final dictionary that associates each longitude to its average elevation
        return dico_per_long

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = TestProfileView()
    app.mainloop()
