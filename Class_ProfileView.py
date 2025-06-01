import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont


class ProfileView():
    def __init__(self):
        """
        Initialize the profile view for a country.
        
        Parameters:
        - parent: the parent window
        - country_per_long: dictionnary {longitude: average_elevation}
        - sea_level: float (sea will be displayed in blue)
        """
        
        super().__init__()

        self.image = None
        self.photo = None
        self.dico_per_long = {}
        self.max_elevation = 1
        self.sea_level = 0
        self.axis_font = ImageFont.truetype("arial.ttf", size=18)

        self.sky_image = None  # Background image


    def draw_profile(self, frame, width, height, dico_per_long, sea_level):
        """
        Draw the profile view from the elevation, the coordinates and the sea level.

        Parameters
        ----------
        frame : 
            
        width : int
            Width of the profile view
        height : int
            Height of the profile view
        dico_per_long : dict
            Dictionary containing the longitudes and their associated elevation
        sea_level : float
            Sea level for the cocnerned year

        Returns
        -------
        None.

        """
        self.canvas = ctk.CTkCanvas(frame, width=width, height=height, bg="white")
        self.canvas.pack(fill=ctk.BOTH, expand=True)
        
        self.dico_per_long = dict(sorted(dico_per_long.items()))
        self.max_elevation = max(self.dico_per_long.values(), default=1)
        self.sea_level = sea_level
        self.load_sky_image() #Background image
        self.redraw()
        
        self.canvas.bind("<Configure>", self.on_resize)
        
    # original code for that has now been replaced with redraw
    # def draw_profile(self):
    #     margin_x = 20       # horizontal margin (on left and right) -nb of pixels
    #     margin_y = 20       # vertical margin (on top and bottom) -nb of pixels
    #     space_x = 5         # horizontal space between each longitude point -nb of pixels
    #     sea_height = 20     # height of the blue sea at the bottom -nb of pixels

    #     # determine highest elevation to set canvas height
    #     max_elev = max(self.country_per_long.values()) + self.sea_level

    #     # compute canvas size
    #     width = len(self.country_per_long) * space_x + 2 * margin_x
    #     height = max_elev + sea_height + margin_y * 2

    #     # create canvas
    #     self.canvas = tk.Canvas(self.parent, width=width, height=height, bg="white")
    #     self.canvas.pack()

    #     # draw the sea
    #     self.canvas.create_rectangle(0, height - sea_height, width, height, fill="blue", outline="blue")

    #     # draw elevation points
    #     points = []
    #     for i, (longitude, elevation) in enumerate(sorted(self.country_per_long.items())):
    #         x = margin_x + i * space_x
    #         y = height - sea_height - elevation
    #         points.append((x, y))
    #         self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black")

    #     # connect points with lines
    #     for i in range(len(points) - 1):
    #         x0, y0 = points[i]
    #         x1, y1 = points[i + 1]
    #         self.canvas.create_line(x0, y0, x1, y1, fill='green', width=2)

    #     # draw elevation scale
    #     scale_x = width - 10
    #     self.canvas.create_line(scale_x, height - sea_height, scale_x, height - sea_height - max_elev, fill="black")
    #     self.canvas.create_text(scale_x - 5, height - sea_height, text="0 m", font=("comic sans ms", 10), anchor="e")
    #     self.canvas.create_text(scale_x - 5, height - sea_height - max_elev, text=f"{int(max_elev)} m", font=("comic sans ms", 10), anchor="e")
   
    def load_sky_image(self):
        """
        Load a background image.

        Returns
        -------
        None.

        """
        try:
            bg = Image.open("blue.jpg").convert("RGB")
            self.sky_image = bg
        except Exception as e:
            print("Error loading blue.jpg:", e)
            self.sky_image = None #Works without image if issue with it


    def redraw(self):
        """
        Draw the profile view and adapt it to the window's size

        Returns
        -------
        None.

        """
        #Error case
        if not self.dico_per_long:
            return
#-----------------------------Made with help of AI----------------------------#
        img_width = self.canvas.winfo_width()
        img_height = self.canvas.winfo_height()
    
        top_margin = 50     # Reserve 50 pixels at the top
        bottom_margin = 100  # Reserve 100 pixels at the bottom
        usable_height = img_height - top_margin - bottom_margin
        display_max_elevation = self.max_elevation
    
        image = Image.new("RGB", (img_width, img_height), "white")
    
        # Calculate sea level position with top_margin offset
        sea_y = int(top_margin + usable_height * (1 - self.sea_level / display_max_elevation))
    
        # Draw sky
        if self.sky_image and sea_y > top_margin:
            resized_sky = self.sky_image.resize((img_width, sea_y))
            image.paste(resized_sky, (0, 0))
    
        draw = ImageDraw.Draw(image)
    
        # Draw elevation profile
        longs = list(self.dico_per_long.keys())
        elevations = list(self.dico_per_long.values())
    
        min_long = min(longs)
        max_long = max(longs)
        long_range = max_long - min_long if max_long != min_long else 1
    
        points = []
        #Initialize the points' coordinates in adequation with the window's size
        for i, lon in enumerate(longs):
            x = int((lon - min_long) / long_range * img_width)
            elev = elevations[i]
            y = int(top_margin + usable_height * (1 - elev / display_max_elevation))
            points.append((x, y))
    
        if points:
            fill_area = points + [(points[-1][0], img_height), (points[0][0], img_height)]
            #Draw the polygon that shapes the land 
            draw.polygon(fill_area, fill=(0, 102, 51))
    
        draw.line([(0, sea_y), (img_width, sea_y)], fill="blue", width=2)
    
        # Below-sea overlay
        overlay = Image.new("RGB", (img_width, img_height), (0, 0, 255))
        mask = Image.new("L", (img_width, img_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rectangle([(0, sea_y), (img_width, img_height)], fill=80)
        image = Image.composite(overlay, image, mask)
    
        draw = ImageDraw.Draw(image)
    
        # Draw white vertical strip (5% of width)
        bar_width = 100
        draw.rectangle([(0, 0), (bar_width, img_height)], fill="white")
    
        # Y-axis ticks every 200 meters
        tick_interval = 200
        max_tick_value = ((self.max_elevation // tick_interval) + 1) * tick_interval
        
        #Indicate the meters so that the user can see the elevation's value
        tick_value = 0
        while tick_value <= max_tick_value:
            y = int(top_margin + usable_height * (1 - tick_value / display_max_elevation))
            draw.text((12, y - 7), f"{tick_value} m", fill="black", font=self.axis_font)
            draw.line([(bar_width - 10, y), (bar_width, y)], fill="black", width=1)
            tick_value += tick_interval
    
        # Draw sea level tick and label in blue
        #Indicate the value of the see level
        draw.text((bar_width+20, sea_y), f"Sea level: {float(self.sea_level)} m", fill="white", font=self.axis_font)
        #draw.text((bar_width+25, sea_y), f"{int(self.sea_level)} m", fill="white", font=self.axis_font)
    
        # Render image to canvas
        self.image = image
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.image = self.photo  # Keep a reference to avoid garbage collection
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def on_resize(self, event):
        """
        Reinitialize the drawing.

        """
        self.redraw()
