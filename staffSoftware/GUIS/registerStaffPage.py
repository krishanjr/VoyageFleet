import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar, DateEntry

import sys
sys.path.append('.')
from bridgeAPIPages import validate_register_staff_form, validate_register_driver_form
import APIFunctions

FRAME_WIDTH = 400

class StaffRegistrationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        super().__init__(parentPage, **kwargs)        
                
        # Username input
        self.username_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Username")
        self.username_input.grid(row=3, column=0, padx=30, pady=(15, 15))
        
        # Password input
        self.password_input = customtkinter.CTkEntry(self, width=250, show="", placeholder_text="Password")
        self.password_input.grid(row=4, column=0, padx=30, pady=(0, 15))
        

        # email input
        self.email_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Email")
        self.email_input.grid(row=5, column=0, padx=30, pady=(15, 15))

        # firstname input
        self.firstname_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Firs tName")
        self.firstname_input.grid(row=6, column=0, padx=30, pady=(15, 15))

        # lastname input
        self.lastname_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Last Name")
        self.lastname_input.grid(row=9, column=0, padx=30, pady=(15, 15))

        # phonenumber input
        self.phonenumber_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Phone Number")
        self.phonenumber_input.grid(row=10, column=0, padx=30, pady=(15, 15))

        # address input
        self.address_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Address")
        self.address_input.grid(row=11, column=0, padx=30, pady=(15, 15))

        self.doblabel = customtkinter.CTkLabel(self, text="Your Date of Birth",font=customtkinter.CTkFont(size=14))
        self.doblabel.grid(row=12, column=0, sticky="w")
        # dateofBirth input
        self.dateofBirth_input = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010)
        #self.dateofBirth_input.pack(fill="both", expand=True)
        self.dateofBirth_input.grid(row=12, column=0)

        # Gender input
        self.gender_var = customtkinter.StringVar(value="M")
        self.gender_input = customtkinter.CTkComboBox(self, width=250, values=["Male", "Female", "Other"], variable=self.gender_var)
        self.gender_input.grid(row=14, column=0, padx=30, pady=(15, 15))
        self.gender_var.set("Male")

        # Register button
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self.register_event, width=200)
        self.register_button.grid(row=15, column=0, padx=30, pady=(15, 15))

    def register_event(self):
        """Register Button is pressed"""
        gender_input = self.gender_var.get().capitalize()[0]
        
        inputs = {
            "user": {
                "username": self.username_input.get(),
                "email": self.email_input.get(),
                "first_name": self.firstname_input.get(),
                "last_name": self.lastname_input.get(),
                "password": self.password_input.get()
            },
            "phone_number": self.phonenumber_input.get(),
            "address": self.address_input.get(),
            "date_of_birth": str(self.dateofBirth_input.get_date()),
            "gender": gender_input
        }

        validated_inputs = validate_register_staff_form(inputs)
        if not isinstance(validated_inputs, dict):
            return messagebox.showerror('Error',validated_inputs)
        #input is validated now sending to server
        staffAPI = APIFunctions.StaffAPI()
        response = staffAPI.create_staff(validated_inputs)
        print(inputs)      
        if response.status_code == 201:
            # successfully created
            return messagebox.showinfo('User Created', "User of " + self.username_input.get() + " created Successfully")
        return messagebox.showerror('Error', response.json_data)
            
class DriverRegistrationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        super().__init__(parentPage, **kwargs)        
                
        # Username input
        self.username_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Username")
        self.username_input.grid(row=3, column=0, padx=30, pady=(15, 15))
        
        # Password input
        self.password_input = customtkinter.CTkEntry(self, width=250, show="", placeholder_text="Password")
        self.password_input.grid(row=4, column=0, padx=30, pady=(0, 15))
        

        # email input
        self.email_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Email")
        self.email_input.grid(row=5, column=0, padx=30, pady=(15, 15))

        # firstname input
        self.firstname_input = customtkinter.CTkEntry(self, width=250, placeholder_text="First Name")
        self.firstname_input.grid(row=6, column=0, padx=30, pady=(15, 15))

        # lastname input
        self.lastname_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Last Name")
        self.lastname_input.grid(row=7, column=0, padx=30, pady=(15, 15))

        # phonenumber input
        self.phonenumber_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Phone Number")
        self.phonenumber_input.grid(row=8, column=0, padx=30, pady=(15, 15))

        # address input
        self.address_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Address")
        self.address_input.grid(row=9, column=0, padx=30, pady=(15, 15))

        self.doblabel = customtkinter.CTkLabel(self, text="Driver's Date of Birth",font=customtkinter.CTkFont(size=14))
        self.doblabel.grid(row=10, column=0, sticky="w")
        # dateofBirth input
        self.dateofBirth_input = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010)
        #self.dateofBirth_input.pack(fill="both", expand=True)
        self.dateofBirth_input.grid(row=11, column=0)

        # Gender input
        self.gender_var = customtkinter.StringVar(value="M")
        self.gender_input = customtkinter.CTkComboBox(self, width=250, values=["Male", "Female", "Other"], variable=self.gender_var)
        self.gender_input.grid(row=12, column=0, padx=30, pady=(15, 15))
        self.gender_var.set("Male")

        self.license_number_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Licence Number")
        self.license_number_input.grid(row=13, column=0, padx=30, pady=(15, 15))

        self.license_expiry_date_label = customtkinter.CTkLabel(self, text="Licence Expiry Date",font=customtkinter.CTkFont(size=14))
        self.license_expiry_date_label.grid(row=14, column=0, sticky="w")
        self.license_expiry_date = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2024)
        self.license_expiry_date.grid(row=15, column=0)

        # Register button
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self.register_event, width=200)
        self.register_button.grid(row=16, column=0, padx=30, pady=(15, 15))

    def register_event(self):
        """Register Button is pressed"""
        gender_input = self.gender_var.get().capitalize()[0]
        
        inputs = {
            "user": {
                "username": self.username_input.get(),
                "email": self.email_input.get(),
                "first_name": self.firstname_input.get(),
                "last_name": self.lastname_input.get(),
                "password": self.password_input.get()
            },
            "phone_number": self.phonenumber_input.get(),
            "address": self.address_input.get(),
            "date_of_birth": str(self.dateofBirth_input.get_date()),
            "gender": gender_input,
            "license_number": self.license_number_input.get(),
            "license_expiry_date": str(self.license_expiry_date.get_date())
        }

        validated_inputs = validate_register_driver_form(inputs)
        if not isinstance(validated_inputs, dict):
            return messagebox.showerror('Error', validated_inputs)
        #input is validated now sending to server
        staffAPI = APIFunctions.DriverAPI()
        response = staffAPI.create_driver(validated_inputs)
        print(inputs)      
        if response.status_code == 201:
            # successfully created
            return messagebox.showinfo('User Created', "User of " + self.username_input.get() + " created Successfully")


        else:
            # todo add errorFrame to show error. Best for UI to show error
            return messagebox.showerror('Error', response.json_data)
            


class RegistrationFrame(customtkinter.CTkScrollableFrame):
    """Class representing the Registration Frame"""
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        # initiate register frame
        #kwargs["width"] = FRAME_WIDTH
        #kwargs["corner_radius"] = 0
        super().__init__(parentPage, **kwargs)

        #self.corner_radius = 15
        # Register label
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Register",font=customtkinter.CTkFont(size=24, weight="bold", slant="roman", family="Roboto"))
        self.label.grid(row=0, column=0, sticky="w")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, rowspan = 2, columnspan = 2 , sticky="nswe")
        self.tabview.add("Support Staff")
        self.tabview.add("Driver")
        self.tabview.tab("Support Staff").grid_columnconfigure(0, weight=3)  # configure grid of individual tabs
        self.tabview.tab("Driver").grid_columnconfigure(0, weight=3)

        supportStaffTab = self.tabview.tab("Support Staff")
        driverTab = self.tabview.tab("Driver")
        
        self.supportStaffRegistrationFrame = StaffRegistrationFrame(supportStaffTab)
        self.supportStaffRegistrationFrame.grid(row=0, column=0, sticky="nswe")

        self.driverRegistrationFrame = DriverRegistrationFrame(driverTab)
        self.driverRegistrationFrame.grid(row=0, column=0, sticky="nswe")

        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Driver"), text="CTkLabel on Tab 2")
        # self.label_tab_2.grid(row=0, column=0,sticky="nswe")




