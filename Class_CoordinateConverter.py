class CoordinateConverter:
    def __init__(self):
        pass

    def canvas_to_geo(self, x, y, canvas, base_image, lats, lons, pan_x, pan_y, zoom, lat_indices, lon_indices):
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


