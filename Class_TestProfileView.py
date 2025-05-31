import customtkinter as ctk
import pandas as pd
from Class_ProfileView import ProfileView


class TestProfileView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Profile View Test")
        self.geometry("1000x700")

        # Create main frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create ProfileView instance
        self.profile_view = ProfileView()

        try:
            self.dico_per_long = self.build_dico_per_long()
        except Exception as e:
            print("Error loading CSV:", e)
            self.dico_per_long = {}

        # Only draw if there's valid data
        if self.dico_per_long:
            self.profile_view.draw_profile(
                self.frame, 
                width=800, 
                height=500, 
                dico_per_long=self.dico_per_long, 
                sea_level=0.2  # realistic sea level in meters
            )
        else:
            error_label = ctk.CTkLabel(self.frame, text="Error: No elevation data loaded.")
            error_label.pack(pady=20)

    def build_dico_per_long(self):
        fichier_csv = 'fr_mainland_only.csv'

        # Load CSV file
        coordinates = pd.read_csv(fichier_csv, encoding='utf-8', delimiter=",")

        # Round longitudes to 1 decimal place
        coordinates['Longitude'] = coordinates['Longitude'].round(1)

        # Group by longitude and compute average elevation
        grouped = coordinates.groupby('Longitude')['Elevation'].mean()

        # Build dictionary of {longitude: average_elevation}
        dico_per_long = {lon: round(avg_elev) for lon, avg_elev in grouped.items()}

        return dico_per_long


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = TestProfileView()
    app.mainloop()
