import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar

import sys
sys.path.append('.')
import APIFunctions

class SidebarFrame(customtkinter.CTkFrame):
    width = (int)(1280/1)
    height = 768

    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        # initiate sidebar frame
        kwargs["width"] = self.width
        kwargs["height"] = self.height
        super().__init__(parentPage, **kwargs)
        row = 0
        self.logo_label = customtkinter.CTkLabel(self, text="Voyage Fleet", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=row, column=0, padx=20, pady=(20, 10))
        row+=1
        name = "Welcome " + self.parentPage.userDetail["user"]["first_name"] + " " + self.parentPage.userDetail["user"]["last_name"]
        self.usergreet_label = customtkinter.CTkLabel(self, text=name, font=customtkinter.CTkFont(size=13, weight="bold"))
        self.usergreet_label.grid(row=row, column=0, padx=20, pady=(20, 10))
        row+=1
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="Booking History",  command=lambda : self.change_frame_event("ViewBookingsFrame"))
        self.sidebar_button_1.grid(row=row, column=0, padx=20, pady=10)
        row+=1
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="List all Vehicles",  command=lambda : self.change_frame_event("VehicleListForm"))
        self.sidebar_button_1.grid(row=row, column=0, padx=20, pady=10)
        row+=1
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="Add New Vehicle",  command=lambda : self.change_frame_event("VechicleRegistrationFrame"))
        self.sidebar_button_1.grid(row=row, column=0, padx=20, pady=10)
        row+=1
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="Add New Staff",  command=lambda : self.change_frame_event("RegistrationFrame"))
        self.sidebar_button_1.grid(row=row, column=0, padx=20, pady=10)


        
        row=8
        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=row, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                command=self.change_appearance_mode_event)
        row+=1
        self.appearance_mode_optionemenu.grid(row=row, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        row+=1
        self.scaling_label.grid(row=row, column=0, padx=20, pady=(10, 0))
        row+=1
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=row, column=0, padx=20, pady=(10, 20))


    def change_frame_event(self, frame_name):
        self.parentPage.change_frame(frame_name)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    
class SidebarPage(customtkinter.CTk):
    width = 1280          # width
    height = 768         # height
    def __init__(self):
        super().__init__()

        self.title("Voyage Fleet Side Bar")
        self.geometry(f"{self.width}x{self.height}")


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebarFrame = SidebarFrame(self, width=140, corner_radius=0)
        #self.frames["loginFrame"].grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self,  border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

if __name__ == "__main__":

    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


    app = SidebarPage()
    app.mainloop()