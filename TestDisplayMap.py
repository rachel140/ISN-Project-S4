"""
elevation_map_zoom2.py

Loads a NetCDF elevation dataset (ETOPO), builds a full‑resolution
RGB bitmap, and displays it in a Tkinter window that you can:
  • resize freely (image always fills the canvas)
  • zoom in/out with the mouse wheel, centered at the cursor
"""

import netCDF4 as nc
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


class Test:
    def __init__(self, file_name, base_width=1200, base_height=600):
        """
        :param file_name: path to ETOPO NetCDF file
        :param base_width: width (px) at which to pre‑generate the map
        :param base_height: height (px) at which to pre‑generate
        """
        self.netcdf_file = file_name
        self.base_width = base_width
        self.base_height = base_height

        # current zoom level (1.0 = 100%)
        self.zoom = 1.0
        # pan offset of the image on the canvas
        self.pan_x = 0
        self.pan_y = 0

        # these will be set in generate_base_image()
        self.base_image = None
        self.photo      = None

    def generate_base_image(self, water_level=112):
        """Load once and build a PIL.Image of size (base_width x base_height)."""
        if self.base_image is not None:
            return

        with nc.Dataset(self.netcdf_file) as ds:
            lats  = ds.variables['lat'][:]
            lons  = ds.variables['lon'][:]
            elevs = ds.variables['z'][:]

        # map north→top by reversing latitude indices
        lat_idx = np.linspace(len(lats)-1, 0, self.base_height).round().astype(int)
        lon_idx = np.linspace(0, len(lons)-1, self.base_width).round().astype(int)
        elev_sub = elevs[lat_idx[:,None], lon_idx[None,:]]

        # build RGB array: blue if below water, green if above
        arr = np.empty((self.base_height, self.base_width, 3), dtype=np.uint8)
        below = elev_sub < water_level
        arr[...,0] = 0
        arr[...,1] = np.where(below, 0, 255)
        arr[...,2] = np.where(below, 255, 0)

        self.base_image = Image.fromarray(arr, mode='RGB')
        print(f"[INFO] Base image generated at {self.base_width}×{self.base_height}px")

    def redraw(self):
        """Scale & draw the base_image at (pan_x, pan_y)."""
        if self.base_image is None:
            return

        # current canvas size
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # scaled image size
        tw = max(1, int(w * self.zoom))
        th = max(1, int(h * self.zoom))

        # resize & convert to PhotoImage
        img = self.base_image.resize((tw, th), Image.NEAREST)
        self.photo = ImageTk.PhotoImage(img)

        # draw
        self.canvas.delete("all")
        self.canvas.create_image(int(self.pan_x), int(self.pan_y),
                                 anchor=tk.NW, image=self.photo)

    def on_resize(self, event):
        """
        Window was resized → re‑center the image (so it still fills the canvas).
        """
        w, h = event.width, event.height
        tw = int(w * self.zoom)
        th = int(h * self.zoom)

        # center it
        self.pan_x = (w - tw) / 2
        self.pan_y = (h - th) / 2
        self.redraw()

    def on_zoom(self, event):
        """
        Mouse wheel: zoom in/out by 10%, *around* the pointer position.
        """
        # choose zoom factor
        factor = 1.1 if event.delta > 0 else 0.9
        old_zoom = self.zoom
        new_zoom = max(0.1, min(old_zoom * factor, 10.0))

        # pointer position in canvas coords
        mx, my = event.x, event.y

        # which image‑pixel is under the pointer?
        ix = (mx - self.pan_x) / old_zoom
        iy = (my - self.pan_y) / old_zoom

        # update zoom
        self.zoom = new_zoom

        # compute new pan so (ix,iy) still sits at (mx,my)
        self.pan_x = mx - ix * new_zoom
        self.pan_y = my - iy * new_zoom

        self.redraw()

    def create_canvas(self, width=1200, height=600, water_level=112):
        """Build the Tk window, generate the map, and bind events."""
        self.generate_base_image(water_level)

        self.root = tk.Tk()
        self.root.title("Elevation Map (zoom & resize)")

        # make a resizable canvas
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # initialize pan so the image exactly fills the starting window
        self.pan_x = 0
        self.pan_y = 0

        # bind resize & zoom
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<MouseWheel>",   self.on_zoom)

        # initial draw
        self.redraw()
        self.root.mainloop()


if __name__ == "__main__":
    nc_file = "ETOPO_2022_v1_60s_N90W180_bed.nc"
    tester = Test(nc_file, base_width=1200, base_height=600)
    tester.create_canvas(width=1200, height=600, water_level=112)
