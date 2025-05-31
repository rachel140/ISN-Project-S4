import netCDF4 as nc               
import numpy as np                
from PIL import Image, ImageTk 
import customtkinter as ctk
import tkinter as tk



class SecondaryView:
    def __init__(self, controller):
        self.controller = controller
        self.netcdf_file = "ETOPO_2022_v1_60s_N90W180_bed.nc"
        
        # These will be set when generate_base_image() is called
        self.base_image = None      # PIL Image representing the map with sea level coloring
        self.photo = None           # Tkinter-compatible PhotoImage for displaying on canvas
        self.zoom = 1.0             # Zoom scale factor (1.0 = no zoom)
        self.pan_x = 0              # Horizontal pan offset for image drawing
        self.pan_y = 0              # Vertical pan offset for image drawing
        self.last_water_level = None  # Store the last used water level to avoid unnecessary regeneration

    def generate_base_image(self, base_width, base_height, sea_level):
        """
        Generate the base image (PIL.Image) sized (base_width x base_height) showing land and sea colors.
        Uses elevation data from netCDF file to color pixels blue if below sea level, green if above.
        Only regenerates if water level changed since last call.
        """
        # If image already generated and water level hasn't changed, no need to regenerate
        if self.base_image is not None and self.water_level == sea_level:
            return
        
        # Get current sea level for given year and scenario
        self.water_level = sea_level
        
        # In case the canvas width and height in mainframe are not available
        if base_width <= 1 or base_height <= 1:
            base_width, base_height = 800, 600
        
        # Open the netCDF elevation dataset and read latitude, longitude, and elevation arrays
        with nc.Dataset(self.netcdf_file) as ds:
            lats = np.array(ds.variables['lat'])   # 1D array of latitudes
            lons = np.array(ds.variables['lon'])  # 1D array of longitudes
            elevs = np.array(ds.variables['z'])     # 2D array of elevations (lat x lon)
        
        # Save lat/lon arrays to instance variables for coordinate converter (canvas to geo)
        self.lats = lats
        self.lons = lons
        
        # reverse the lattitude (north to south) to match image coordinates and space evenly coordinates
        lat_indices = np.linspace(len(lats)-1, 0, base_height).round().astype(int)
        lon_indices = np.linspace(0, len(lons)-1, base_width).round().astype(int)
        
        self.lat_indices = lat_indices #useful later for the canvas coordinate to geographical coordinate
        self.lon_indices = lon_indices

        
        # Create dictionnary with elev as key and lat lon as values
        #-------------------------original code-------------------------------#
        # elev = np.zeros((base_height, base_width)) #like initialising dico
        # for i in range(base_height):
        #     for j in range(base_width):
        #         elev[i, j] = elevs[lat_indices[i], lon_indices[j]]

        #------------------------improved by AI-------------------------------#
        elev = elevs[lat_indices[:, None], lon_indices[None, :]]
        print(f"[DEBUG] Elevation stats: min={np.min(elev)}, max={np.max(elev)}, mean={np.mean(elev)}")


        # Create an empty array for the RGB image data (height, width, 3 color channels)
        array = np.empty((base_height, base_width, 3), dtype=np.uint8)
        
        # define the colour depending on whether above or below water
        water_rgb = (25, 25, 112)
        land_rgb= (94, 200, 80) #very dark  (31, 120, 50), kinda blue (80, 200, 120) 
        below = (elev <= self.water_level)
        print(f"[DEBUG] Number of below-sea-level points: {np.sum(below)} out of {below.size}")

        array[below] = water_rgb
        array[~below] = land_rgb
    
        #array[..., 0] = 0                       # Set red channel to zero everywhere (no red)
        #array[..., 1] = np.where(below, 0, 255) # Set green channel: 255 where above water, 0 where below
        #array[..., 2] = np.where(below, 255, 0) # Set blue channel: 255 where below water, 0 where above

        # Create a PIL Image from the RGB numpy array
        self.base_image = Image.fromarray(array, mode='RGB')

    def redraw(self):
        """
        Redraw the base image on the canvas, applying zoom and pan offsets.
        This method handles scaling the base image to fit current zoom and placing it
        correctly on the canvas based on pan_x and pan_y.
        """
        # If no base image yet, no drawing needed
        if self.base_image is None:
            return

        # Clear previous drawings on canvas
        self.canvas.delete("all")
        
        #------we could have used self.x and self.h because we are------------#
        #------reusing them in on resize but as we need to redefine-----------#
        #------them for each resize it would be pointless to do so------------#
        
        # Get current canvas size (width and height in pixels)
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Calculate the scaled image size by applying current zoom factor
        new_w = max(1, int(w * self.zoom))  # width after zoom, at least 1 pixel
        new_h = max(1, int(h * self.zoom))  # height after zoom, at least 1 pixel

        # resize the baseimage using nearest neighbour method (=fastest but blocky, use Image.BICUBIC for best quality)
        resized_base_image = self.base_image.resize((new_w, new_h), Image.NEAREST)
        
        # Convert the resized PIL image into a Tkinter-compatible PhotoImage
        self.map_photo = ImageTk.PhotoImage(resized_base_image)
        
        # Draw the image at current pan position, anchoring at the top-left corner (NW)
        self.canvas.create_image(int(self.pan_x), 
                                 int(self.pan_y),
                                 anchor="nw", 
                                 image=self.map_photo)

    def on_resize(self, event):
        """
        Handle window resize events by recalculating pan offsets to center the zoomed image
        within the new canvas size, then redraw.
        """
        w, h = event.width, event.height      # New size of the canvas
        new_w = int(w * self.zoom)            # Width of the zoomed image
        new_h = int(h * self.zoom)            # Height of the zoomed image

        # Calculate pan offsets to center the image in the canvas after resizing
        self.pan_x = (w - new_w) / 2
        self.pan_y = (h - new_h) / 2
        
        # Redraw the canvas with updated pan
        self.redraw()

    def on_zoom(self, event):
        """
        Handle mouse wheel events for zooming in and out.
        Zoom occurs centered on the mouse pointer to create intuitive zoom behavior.
        Prevents zooming out beyond fitting the image to the canvas.
        """
        if self.base_image is None:
            return
#----------------------------Created with help of AI--------------------------#

        # Update canvas geometry info to get current size
        self.canvas.update_idletasks()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
    
        # Get base image original size
        img_w, img_h = self.base_image.size
    
        # Calculate minimum zoom factors needed to ensure image is at least as large as canvas
        min_zoom_x = canvas_w / img_w
        min_zoom_y = canvas_h / img_h
        min_zoom = max(min_zoom_x, min_zoom_y, 0.01)  # Ensure min_zoom is never less than 0.01
    
        # Determine zoom direction and magnitude: 1.1x zoom in, 0.9x zoom out
        factor = 1.1 if event.delta > 0 else 0.9
        old_zoom = self.zoom
        
        # Clamp new zoom to range [min_zoom, 10.0]
        new_zoom = max(min_zoom, min(old_zoom * factor, 10.0))
    
        # Mouse pointer location in canvas coordinates
        mx, my = event.x, event.y
    
        # Calculate position in the image coordinates under the mouse pointer
        ix = (mx - self.pan_x) / old_zoom
        iy = (my - self.pan_y) / old_zoom
    
        # Update zoom factor
        self.zoom = new_zoom
    
        # Adjust pan so that the point under the mouse remains fixed after zooming
        self.pan_x = mx - ix * new_zoom
        self.pan_y = my - iy * new_zoom
    
        # Redraw the image with new zoom and pan
        self.redraw()

    def on_click(self, event):
        # Convert click position to image coordinates
        self.x = int((event.x - self.pan_x) / self.zoom)
        self.y = int((event.y - self.pan_y) / self.zoom) 
        
        print(f"Clicked at: ({self.x}, {self.y})")
        self.controller.create_profile_map()
        
    def create_map(self, frame, width, height, sea_level):
        """
        Create and set up the Tkinter canvas with the base image loaded and display it.
        Also binds resize and zoom events for interactive control.
        """
        print(f"[SECONDARYVIEW] Generating image with sea level: {sea_level}")
        # Generate or update the base image for the given parameters
        self.generate_base_image(width, height, sea_level)

        # Create a Tkinter Canvas widget in the provided parent frame
        self.canvas = tk.Canvas(frame, width=width, height=height, bg="white")
        self.canvas.pack(fill=ctk.BOTH, expand=True)

        # Bind the canvas size change event to on_resize for dynamic resizing behavior
        self.canvas.bind("<Configure>", self.on_resize)
        
        # Bind mouse wheel events to on_zoom for zooming functionality
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        
        #Bind the canvas to a click on the map
        self.canvas.bind("<Button-1>", self.on_click)
        
        print("Map created, showing shape:", self.base_image.size)

        # Initial drawing of the map on the canvas
        self.redraw()
