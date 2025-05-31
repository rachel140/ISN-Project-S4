import datetime
import customtkinter as ctk

from Class_SecondaryView import SecondaryView


class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("World Map")
        self.geometry("900x600")
        ctk.set_appearance_mode("system")

        # parameters
        current_year = datetime.datetime.now().year
        self.rounded_year = min(3000, max(2000, 5 * round(current_year / 5)))
        self.configure(fg_color="midnight blue")
        self.tfc = "white"                # top frame colour
        self.cfc = "midnightblue"         # center frame colour
        self.bfc = "lightblue"            # bottom and right frame colour
        self.ffc = "azure"               # foreground frame colour
        
        self.bc = "steelblue"
        self.hbc = "dodgerblue"

        self.font = "times"
        self.police = 12

        # methods
        self.controller = controller
        self.secondary_view = SecondaryView(self.controller)

        self.create_widget()
        #self.controller.set_views(self, self.secondary_view)



    def create_widget(self):
#-----------------------------------------------------------------------------#
#### ------------------------------- Frames ------------------------------ ####
#-----------------------------------------------------------------------------#

#### ----------------------------- Top Frame ----------------------------- ####
        self.frame_top = ctk.CTkFrame(self,  fg_color=self.tfc)
        self.frame_top.pack(side='top', fill='x')

        self.title_label = ctk.CTkLabel(self.frame_top,
                                       text="The Sea Level Across the Years",
                                       font=ctk.CTkFont(family=self.font,
                                                        size=18,
                                                        weight="bold"
                                                        )
                                       )
        self.title_label.pack()

#### --------------------------- Bottom Frames --------------------------- ####
        self.frame_bottom = ctk.CTkFrame(self, fg_color=self.cfc)
        self.frame_bottom.pack(side='bottom', fill='x')
#### ------------------------- Bottom Left Frame ------------------------- ####
        self.frame_bottom_left = ctk.CTkFrame(self.frame_bottom,
                                              fg_color=self.bfc)
        self.frame_bottom_left.pack(side='left',
                                    fill="both",
                                    padx=5, pady=5)

        # Year (label)
        self.year_label = ctk.CTkLabel(self.frame_bottom_left,
                                       text="Please select a year:",
                                       font=ctk.CTkFont(family=self.font,
                                                        size=self.police,
                                                        )
                                       )
        self.year_label.grid(row=0, column=0, columnspan=2)

        # Year value display (label)
        self.year_value_label = ctk.CTkLabel(self.frame_bottom_left,
                                             text=str(self.rounded_year),
                                             font=ctk.CTkFont(family=self.font,
                                                              size=self.police,
                                                              )
                                             )
        self.year_value_label.grid(row=1, column=0, columnspan=2)

        # Year slider (scale)
        self.year_scale = ctk.CTkSlider(self.frame_bottom_left,
                                        from_=1950, to=3000,
                                        number_of_steps=(3000-1950)//5, #The evolution of the map and the associated sea level can only be seen for every 5 years (i.e, for 2020, 2025, 2030...)
                                        command=self.on_scale_change,
                                        width=200
                                        )
        # Set initial year
        self.year_scale.set(self.rounded_year)
        self.year_scale.grid(row=2, column=0, columnspan=2, pady=5)

        # Plus/minus (button)
        self.decrease_button = ctk.CTkButton(self.frame_bottom_left,
                                             text="-5",
                                             font=ctk.CTkFont(family=self.font,
                                                              size=self.police,
                                                              ),
                                             fg_color=self.bc,
                                             hover_color=self.hbc,
                                             width=50,
                                             command=self.decrease_scale
                                             )
        self.decrease_button.grid(row=3, column=0, pady=5)

        self.increase_button = ctk.CTkButton(self.frame_bottom_left,
                                             text="+5",
                                             font=ctk.CTkFont(family=self.font,
                                                              size=self.police,
                                                              ),
                                             fg_color=self.bc,
                                             hover_color=self.hbc,
                                             width=50,
                                             command=self.increase_scale
                                             )
        self.increase_button.grid(row=3, column=1, pady=5)

    # Sea level
        self.sea_level_title = ctk.CTkLabel(self.frame_bottom_left,
                                            text="Sea level:",
                                            font=ctk.CTkFont(family=self.font,
                                                             size=self.police,
                                                             ),
                                            )
        self.sea_level_title.grid(row=1, column=3, padx=5)

        self.sea_level_label = ctk.CTkLabel(self.frame_bottom_left,
                                            text="0.254 m",
                                            font=ctk.CTkFont(family=self.font,
                                                             size=self.police,
                                                             ),
                                            )
        self.sea_level_label.grid(row=2, column=3, padx=5)


#### ------------------------ Bottom Center Frame ------------------------ ####
        self.frame_bottom_center = ctk.CTkFrame(self.frame_bottom, fg_color=self.bfc)
        self.frame_bottom_center.pack(side='left',
                                      expand=True,
                                      fill='both',
                                      padx=5, pady=5)

        # IPCC (label)
        self.ipcc_label = ctk.CTkLabel(self.frame_bottom_center,
                                       text="Choose your IPCC Scenario:",
                                       font=ctk.CTkFont(family=self.font,
                                                        size=self.police,
                                                        ),
                                       )
        #self.ipcc_label.grid(row=0, column=0)
        self.ipcc_label.pack(pady=10)

            # IPCC (radiobutton)
        self.ipcc_choice_var = ctk.IntVar(value=4)
        values = {"IPCC-1": 1, "IPCC-2": 2, "IPCC-3": 3, "IPCC-4": 4}
        for i, (text, value) in enumerate(values.items()):
            rb = ctk.CTkRadioButton(self.frame_bottom_center,
                                    text=text,
                                    font=ctk.CTkFont(family=self.font,
                                                     size=self.police,
                                                     ),
                                    variable=self.ipcc_choice_var,
                                    value=value)
            rb.pack(pady=5)
            #rb.grid(row=i + 1, column=0, pady=2)

#### ------------------------ Bottom Right Frame ------------------------- ####
        self.frame_bottom_right = ctk.CTkFrame(self.frame_bottom, fg_color=self.bfc)
        self.frame_bottom_right.pack(side='left',
                                     expand=True,
                                     fill='both',
                                     padx=5, pady=5)

    # Generate map (button)
        self.generate_button = ctk.CTkButton(self.frame_bottom_right,
                                             text="Generate map",
                                             font=ctk.CTkFont(family=self.font,
                                                              size=self.police,
                                                              ),
                                             fg_color=self.bc,
                                             hover_color=self.hbc,
                                             command=self.show_map
                                             )
        self.generate_button.pack(pady=25)

    # Show Refugees (button)
        self.generate_refugees = ctk.CTkButton(self.frame_bottom_right,
                                               text="Show refugees",
                                               font=ctk.CTkFont(family=self.font,
                                                                size=self.police,
                                                                ),
                                               fg_color=self.bc,
                                               hover_color=self.hbc,
                                               command=self.count_refugees
                                               )
        self.generate_refugees.pack(pady=5)

    #Show refugees (label)

        self.show_refugees = ctk.CTkLabel(self.frame_bottom_right,
                                          text="",
                                          font=ctk.CTkFont(family=self.font,
                                                           size=self.police,
                                                           ),
                                          )
        self.show_refugees.pack()

    # Initialize sea level label
        self.on_scale_change(self.rounded_year)
#### ------------------------- Right Side Frame -------------------------- ####
        self.frame_right = ctk.CTkFrame(self, width=300, fg_color=self.bfc)
        self.frame_right.pack(side='right', anchor='n', fill='y')

        self.view_mode_label = ctk.CTkLabel(self.frame_right,
                                            text="Current View Mode:",
                                            font=ctk.CTkFont(family=self.font,
                                                             size=self.police,
                                                             ),
                                            )
        self.view_mode_label.pack(pady=5)

        self.view_mode_value = ctk.CTkLabel(self.frame_right,
                                            text='Nothing generated',
                                            font=ctk.CTkFont(family=self.font,
                                                             size=self.police,
                                                             weight="bold"),
                                            fg_color=self.ffc,
                                            width=100
                                            )
        self.view_mode_value.pack()

        self.view_mode_exp = ctk.CTkLabel(self.frame_right,
                                          text="",
                                          font=ctk.CTkFont(family=self.font,
                                                           size=self.police,
                                                           )
                                          )
        self.view_mode_exp.pack(pady=10)


        self.exit_profile_button = ctk.CTkButton(self.frame_right,
                                                 fg_color=self.bfc,
                                                 hover_color=self.bfc,
                                                 text="",
                                                 font=ctk.CTkFont(family=self.font,
                                                                  size=self.police,
                                                                  ),
                                                 command=self.exit_profile_view,
                                                 )
        self.exit_profile_button.pack(pady=20)


#### ------------------------- Center (Map) Frame ------------------------ ####
        self.frame_map = ctk.CTkFrame(self,
                                      fg_color=self.cfc,
                                      width=300, height=200
                                      )
        self.frame_map.pack(fill='both', expand=True)
        self.frame_map.pack_propagate(False)

        self.placeholder_label = ctk.CTkLabel(self.frame_map,
                                              text="You have not loaded a map yet.\n \n Side note: Please be patient during the generation process as there is a lot of data to load, we are currently working on the optimisation.\n  \n Once you have loaded the map in the top view, you can click on a country to get the profile view. \n Note: This feature currently works only for France, we apologise for any inconvenience.",
                                              text_color="white",
                                              font=ctk.CTkFont(family=self.font,
                                                               size=self.police,
                                                               ),
                                              )
        self.placeholder_label.pack(expand=True)
        self.loading_label = ctk.CTkLabel(self.frame_map,
                                          text="Map is loading...",
                                          text_color="white",
                                          font=ctk.CTkFont(family=self.font,
                                                           size=self.police,
                                                           ),
                                          )


#-----------------------------------------------------------------------------#
#### ------------------------------ Methods ------------------------------ ####
#-----------------------------------------------------------------------------#
    def on_scale_change(self, value):
        """
        Adapt the year entered by the user for a one that is a multiple of 5 (i.e, 2020, 2025...).
        Retrieve the sea level (computed in the other classes' functions) and display it to the user.

        Parameters
        ----------
        value : int
            Year entered by the user

        Returns
        -------
        None.

        """
        year = int(round(float(value) / 5) * 5)  # to have step of 5 on scale
        self.year_value_label.configure(text=str(year))
        sea_level = round(self.controller.get_sea_level(self.get_user_year(), int(self.get_ipcc_value())), 3)
        self.sea_level_label.configure(text=f"{sea_level} m")

    def increase_scale(self):
        """
        Increases the year on the scale by 5.

        Returns
        -------
        None.

        """
        val = self.year_scale.get()
        new_val = min(3000, val + 5)
        self.year_scale.set(new_val)
        self.on_scale_change(new_val)

    def decrease_scale(self):
        """
        Decreases the year on the scale by 5.

        Returns
        -------
        None.

        """
        val = self.year_scale.get()
        new_val = max(1950, val - 5)
        self.year_scale.set(new_val)
        self.on_scale_change(new_val)

    def get_ipcc_value(self):
        """
        Store the user's choice of scenario.

        Returns
        -------
        int
            Chosen scenario

        """
        return int(self.ipcc_choice_var.get())

    def get_user_year(self):
        """
        Retrieve the year chosen by the user and return it rounded for it to correspond to a step of 5 years.

        Returns
        -------
        int
            Chosen year

        """
        return int(round(self.year_scale.get() / 5) * 5)

    def show_map(self):
        """
        Display the map as well as a loading label while waiting.

        Returns
        -------
        None.

        """
        # Show the loading label
        self.loading_label.place(relx=0.5, rely=0.5, anchor='center')

        # Remove placeholder if it exists
        if self.placeholder_label.winfo_exists():
            self.placeholder_label.destroy()

        # Let the GUI update so the loading label is visible
        self.update_idletasks()

        # Use .after() to delay just enough to show loading before heavy tasks
        self.after(1, self.generate_map_canvas)

    def generate_map_canvas(self):
        """
        Create the map.

        Returns
        -------
        None.

        """

        self.controller.top_or_side()

        self.loading_label.place_forget()

    def count_refugees(self):
        amount = int(self.controller.count_refugees())
        if 2021 < self.year_scale.get() < 2025:
            self.show_refugees.configure(text=f"In {self.year_scale.get()}, there were {amount} climatic refugees.")
        elif self.year_scale.get() == 2025:
            self.show_refugees.configure(text=f"In {self.year_scale.get()}, there are {amount} climatic refugees.")
        elif 2025 < self.year_scale.get() < 2523:
            self.show_refugees.configure(text=f"In {self.year_scale.get()}, there will be {amount} climatic refugees.")
        else:
            self.show_refugees.configure(text="We cannot tell how many climatic refugees there are.\n Please select a year between 2022 and 2525.")

    def change_mode_value(self, value):
        self.view_mode_value.configure(text=f"{value}")
        if value == "profile":
            self.exit_profile_button.configure(fg_color=self.bc,
                                               hover_color=self.hbc,
                                               text="Exit profile view")
            self.view_mode_exp.configure(text="In the profile view,\nimagine that you\nare standing on\nEngland and\nlooking at France")
            self.title_label.configure(text="Profile View of France")
        elif value == "top":
            self.exit_profile_button.configure(fg_color=self.bfc,
                                               hover_color=self.bfc,
                                               text="")
            self.view_mode_exp.configure(text="")
            self.title_label.configure(text="The Sea Level Across the Years")
            
    def exit_profile_view(self):
        self.controller.side = "top"
        self.controller.top_or_side()

# if __name__ == "__main__":
#     app = MainView()
#     app.mainloop()
