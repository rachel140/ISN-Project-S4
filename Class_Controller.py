from Class_SeaLevel import SeaLevel
from Class_ElevationData import ElevationData
from Class_ProfileView import ProfileView
from Class_CoordinateConverter import CoordinateConverter
from Class_MainView import MainView

class Controller:

    def __init__(self):
        #files used
        self.world_elevation = "ETOPO_2022_v1_60s_N90W180_bed.nc"
        self.mainland_france_contour = "fr_mainland_contour.csv"
        self.mainland_france = "fr_mainland.csv"

        #adding other classes
        self.sea_level = SeaLevel()
        self.main_view = None
        self.secondary_view = None
        self.profile_view = ProfileView()
        self.coordinate_converter = CoordinateConverter()
        self.elevation_data = ElevationData(self.world_elevation, self.mainland_france, self.mainland_france_contour)
        
        # Create views here and inject controller
        self.main_view = MainView(self)
        self.secondary_view = self.main_view.secondary_view  # already created inside MainView

        # Link views to controller
        self.set_views(self.main_view, self.secondary_view)

        #information for maps:
        self.side = "top"       
        self.reference_elevation = 0.21 #can only calculate refugees starting in 2022 (had elevation of 0.22m at that time)

    def set_views(self, mainview, secondaryview):
        self.main_view = mainview
        self.secondary_view = secondaryview

    @property
    def frame(self):
        return self.main_view.frame_map

    @property
    def width(self):
        return self.main_view.frame_map.winfo_width()

    @property
    def height(self):
        return self.main_view.frame_map.winfo_height()

    @property
    def chosen_year(self):
        return self.main_view.get_user_year()

    @property
    def sea_level_value(self):
        return self.sea_level.retrieve_sea_level(
            self.chosen_year,
            self.main_view.get_ipcc_value()
        )
                                                           

    def count_refugees(self):
        nb_refugees = self.elevation_data.compute_refugees(self.chosen_year,
                                                           self.sea_level_value,
                                                           self.reference_elevation
                                                           )
        return nb_refugees

    def top_or_side(self):
        """
        Define if we want to display to profile view or the global one.

        Returns
        -------
        None.

        """
        if self.side == "top": #The user wants to see the global map
            self.main_view.change_mode_value("top")
            self.create_top_map()
            print(f"[CONTROLLER] Generating image with sea level: {self.sea_level_value} and scenario : {self.main_view.get_ipcc_value()}")

        if self.side == "profile":  #The user wants to see the profile view of a specific country
            self.main_view.change_mode_value("profile")
            self.create_profile_map()

    def create_top_map(self):
        """
        Create a map adapted to the user's choice (reuse of a function from SecondaryView)

        Returns
        -------
        None.

        """
        # Clear old canvas if exists
        for widget in self.main_view.frame_map.winfo_children():
            widget.pack_forget()

        self.secondary_view.create_map(self.frame,
                                       self.width,
                                       self.height,
                                       self.sea_level_value)
        self.side = "top" #Set the parameter to then display the general view of the map
        self.main_view.change_mode_value("top")

    def create_profile_map(self):
        """
        Prepare and draw the profile view of a country for which it is available if the user has clicked on it.
        
        Returns :
        ------- 
        None
        """
        #If the user has clicked on the a country for which the profile view is available
        if self.elevation_data.test_if_point_in(self.get_where_clicked()):
            # Clear old ProfileView if exists
            for widget in self.main_view.frame_map.winfo_children():
                widget.pack_forget()

            # Prepare data: dictionary of elevation with respect to the longitude (for France only)
            dico_per_long = self.elevation_data.build_dico_per_long(self.sea_level_value)


            # Draw profile
            self.profile_view.draw_profile(self.frame,
                                           self.width,
                                           self.height,
                                           dico_per_long,
                                           self.sea_level_value)

            self.side = "profile" #Set the parameter to then display the profile view of the concerned country
            self.main_view.change_mode_value("profile")



    def get_where_clicked(self):
        """
        Retrieve the geographical coordinates (lattitude and longitude) of a point from the x and y coordinates of the window

        Returns
        -------
        lat : float
            Lattitude of the concerned point
        lon : float
            Longitude of the concerned point

        """
        x, y = self.secondary_view.x, self.secondary_view.y
        #canvas_to_geo(self, x, y, canvas, base_image, lats, lons, pan_x, pan_y, zoom, lat_indices, lon_indices):
        lat, lon = self.coordinate_converter.canvas_to_geo(x=x, y=y,
                                                           canvas=self.secondary_view.canvas,
                                                           base_image=self.secondary_view.base_image,
                                                           lats=self.secondary_view.lats,
                                                           lons=self.secondary_view.lons,
                                                           pan_x=self.secondary_view.pan_x,
                                                           pan_y=self.secondary_view.pan_y,
                                                           zoom=self.secondary_view.zoom,
                                                           lat_indices=self.secondary_view.lat_indices,
                                                           lon_indices=self.secondary_view.lon_indices
                                                           )
        print(f"Clicked : {self.secondary_view.x} , {self.secondary_view.y} → received: {x}, {y} → geo: lat={lat:.3f}, lon={lon:.3f}")
        
        return (lat, lon)
    
    def get_sea_level(self, year, scenario):
        """
        Retrieve the sea level from the SeaLevel class and its functions

        Parameters
        ----------
        year : int
            Year choosen by the user to visualize
        scenario : int
            GIEC scenario choosen by the user to visualize

        Returns
        -------
        self.sea_level_value : float
            Sea level for the corresponding year and scenario

        """
        return self.sea_level.retrieve_sea_level(year, scenario)
    
    def run(self):
        self.main_view.mainloop()
        
if __name__ == "__main__":
    app_controller = Controller()
    app_controller.run()
