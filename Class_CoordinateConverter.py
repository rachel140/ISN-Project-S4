class CoordinateConverter:
    def __init__(self):
        pass

    def canvas_to_geo(self, x, y, canvas, base_image, lats, lons, pan_x, pan_y, zoom, lat_indices, lon_indices):
        """
        Converts coordinates (x, y) of a point on the canva with the map of the Earth into real coordinates on Earth (latitude, longitude).

        Parameters
        ----------        
        x : float
            x coordinate on the canvas.
        y : float
            y coordinate on the canvas.
        canvas: canva
            canva containing the image of the Earth (base_image)
        base_image : PIL image 
            image generated using the .nc file with all points on Earth
        lats : numpy arrays
            array of the latitudes, from the .nc file 
        lons : numpy arrays
            array of the longitudes, from the .nc file 
        pan_x : float
            Horizontal pan offset to draw the image
        pan_y : float
            Vertical pan offset to draw the image
        zoom : float
            Zoom scale factor (1.0 = no zoom)
        lat_indices : numpy linspace
            array with regularly spaced values of the latitudes            
        lon_indices : numpy arrays
            array with regularly spaced values of the longitudes        
        
        Returns
        -------
        lat : float
            Latitude of a point on Earth.
        lon : float
            Longitude of a point on Earth.
        """
        # Step 1: Convert canvas (display) coordinates to image pixel coordinates
        image_x = int((x - pan_x) / zoom)
        image_y = int((y - pan_y) / zoom)
    
        # Step 2: Clamp pixel coords within image bounds
        image_x = max(0, min(image_x, base_image.width - 1))
        image_y = max(0, min(image_y, base_image.height - 1))
    
        # Step 3: Map pixel indices back to lat/lon
        lat_index = lat_indices[image_y]
        lon_index = lon_indices[image_x]
    
        # Step 4: Convert to geographic coordinates
        lat = float(lats[lat_index])
        lon = float(lons[lon_index])
    
        return lat, lon


