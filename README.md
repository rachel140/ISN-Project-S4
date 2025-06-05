## **Usage instruction**

### **To run the program**

**To install all the necessary libraries**, write ‘`pip install *library name*`’ 
list of libraries: customtkinter, tkinter, netCDF4, numpy, pandas, pillow, shapely, matplotlib, csv and datetime 
*Restart the kernel*  
**Execute the MainView class**. This will start the main user interface of the simulation. The execution might take some time, 

---

### **To display the map of emerged land**

- **Year Selection**: Use the slider or the arrow buttons to select a year. The selected year is automatically rounded to the nearest multiple of 5.

- **Selecting a Climate Scenario**: Choose one of the four available IPCC scenarios. Each scenario corresponds to a different sea level rise model.

- **Generating the Map**: Click on the **"Generate Map"** button to display the global map showing areas still above sea level, based on the selected year and scenario. This process can be repeated for any other year or scenario.

- **Zooming and Navigating the Map**: Use the mouse scroll wheel to zoom in or out on the map. This allows for closer inspection of specific regions. The image will automatically pan to remain centered during resizing or zooming.

---

### **To display the profile view of France**

Click on **France** on the map to access a profile view showing emerged land with respect to the sea level.  
This view includes a vertical scale with elevation and a sea level line.  
You can change the year thanks to the slider while in this view to observe variations over time.  
To return to the main map, click the **"Quit"** button.

---

### **To compute the number of climate refugees**

Click the **“Show Refugees”** button (available only for years beyond 2022).  
The application calculates and displays the number of people displaced due to land loss from sea level rise, calculated by multiplying the submerged land area on each continent by its average population density.

---

### **To exit the application**

To close the application, simply close the window (top-right **"X"** button).


