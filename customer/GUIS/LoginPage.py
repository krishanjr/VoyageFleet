import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar, DateEntry

import sys
sys.path.append('.')
from bridgeAPIPages import loginCustomer, validate_register_customer_form
import APIFunctions

"""

from utils import configUI
configLoginPageUI = configUI["LoginPage"]
configLoginFrameUI = configLoginPageUI["LoginFrame"]
"""



def gotoDashboard(username, password):
    import DashboardPage
    DashboardPage.Main(username, password)
    #self.parentPage.destroy()   
    exit()

FRAME_WIDTH = 400
# Frame width for Login and Registration Frame

class LoginFrame(customtkinter.CTkScrollableFrame):
    """Class representing the login Frame"""
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        # initiate login frame
        kwargs["width"] = FRAME_WIDTH
        kwargs["corner_radius"] = 60
        super().__init__(parentPage, **kwargs)
        
        # self.corner_radius = 15
        # Login label
        self.label = customtkinter.CTkLabel(self, text="Login",font=customtkinter.CTkFont(size=24, weight="bold", slant="roman", family="Roboto"))
        self.label.grid(row=0, column=0, sticky="w")

        # Username input
        self.username_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Username")
        self.username_input.grid(row=3, column=0, padx=30, pady=(15, 15))
        
        # Password input
        self.password_input = customtkinter.CTkEntry(self, width=250, show="*", placeholder_text="Password")
        self.password_input.grid(row=4, column=0, padx=30, pady=(0, 15))
        
        # Show password checkbox
        self.show_password_var = customtkinter.BooleanVar()
        self.show_password_checkbutton = customtkinter.CTkCheckBox(
            self,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
        )
        self.show_password_checkbutton.grid(
            row=5, column=0, padx=30, sticky="w", pady=(0, 15)
        )
        
        # Login button
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=6, column=0, padx=30, pady=(15, 15))

    def toggle_password_visibility(self):
        """Toggle the visibility of the password input."""
        if self.show_password_var.get():
            self.password_input.configure(show="")
        else:
            self.password_input.configure(show="*")

    def login_event(self):
        """Login Button is pressed"""
        username_input = self.username_input.get()
        password_input = self.password_input.get()
        credential = (username_input, password_input)
        login_resp = loginCustomer(credential=credential)
        if login_resp.status_code != 200:
            #login failed
            # todo add errorFrame to show error. Best for UI to show error
            return messagebox.showerror('Error','Incorrect Username or Password')
        gotoDashboard(self.username_input.get(), self.password_input.get())

        
class RegistrationFrame(customtkinter.CTkScrollableFrame):
    """Class representing the Registration Frame"""
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        # initiate register frame
        kwargs["width"] = FRAME_WIDTH
        kwargs["corner_radius"] = 60
        super().__init__(parentPage, **kwargs)

        self.corner_radius = 15
        # Register label
        self.label = customtkinter.CTkLabel(self, text="Register",font=customtkinter.CTkFont(size=24, weight="bold", slant="roman", family="Roboto"))
        self.label.grid(row=0, column=0, sticky="w")
        
        # Username input
        self.username_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Username")
        self.username_input.grid(row=3, column=0, padx=30, pady=(15, 15))
        
        # Password input
        self.password_input = customtkinter.CTkEntry(self, width=250, show="*", placeholder_text="Password")
        self.password_input.grid(row=4, column=0, padx=30, pady=(0, 15))
        
        # Retype Password input
        self.retype_password_input = customtkinter.CTkEntry(self, width=250, show="*", placeholder_text="Retype-Password")
        self.retype_password_input.grid(row=5, column=0, padx=30, pady=(0, 15))
        
        # Show password checkbox
        self.show_password_var = customtkinter.BooleanVar()
        self.show_password_checkbutton = customtkinter.CTkCheckBox(
            self,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
        )
        self.show_password_checkbutton.grid(
            row=6, column=0, padx=30, sticky="w", pady=(0, 15)
        )

        # email input
        self.email_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Email")
        self.email_input.grid(row=7, column=0, padx=30, pady=(15, 15))

        # firstname input
        self.firstname_input = customtkinter.CTkEntry(self, width=250, placeholder_text="Firs tName")
        self.firstname_input.grid(row=8, column=0, padx=30, pady=(15, 15))

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
                "password": self.password_input.get(),
                "retype_password": self.retype_password_input.get()
            },
            "phone_number": self.phonenumber_input.get(),
            "address": self.address_input.get(),
            "date_of_birth": str(self.dateofBirth_input.get_date()),
            "gender": gender_input
        }

        validated_inputs = validate_register_customer_form(inputs)
        if not isinstance(validated_inputs, dict):
            return messagebox.showerror('Error',validated_inputs)
        #input is validated now sending to server
        customerAPI = APIFunctions.CustomerAPI()
        response = customerAPI.create_customer(validated_inputs)
        print(inputs)      
        if response.status_code == 201:
            # successfully authenticated
            gotoDashboard(self.username_input.get(), self.password_input.get())

        else:
            # todo add errorFrame to show error. Best for UI to show error
            return messagebox.showerror('Error',response.json_data)
            
    def toggle_password_visibility(self):
        """Toggle the visibility of the password input."""
        if self.show_password_var.get():
            self.password_input.configure(show="")            
            self.retype_password_input.configure(show="")
        else:
            self.password_input.configure(show="*")            
            self.retype_password_input.configure(show="*")

class LoginPage(customtkinter.CTk):
    """Class representing the login GUI."""
    width = 1280          # width
    height = 768         # height
    bg_light_image = "Image/Background_gradient.jpg"
    bg_dark_image = "Image/Background_gradient_dark.jpg"
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry(f"{self.width}x{self.height}+0+0")

        #self.grid_columnconfigure((0,1), weight=1)
        # setup background image
        # for caching image during resize
        self.bg_loaded_light_image = Image.open(self.bg_light_image)
        self.bg_loaded_dark_image = Image.open(self.bg_dark_image)
        self.bg_image = customtkinter.CTkImage(light_image=self.bg_loaded_light_image,
                                  dark_image=self.bg_loaded_dark_image,
                                  size=(1280, 768))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
        #self.bg_image_label.grid(row=0, column=0, sticky="")
        self.bg_image_label.place(x=0,y=0)
        self.resize_background(self.width, self.height)

        #self.columnconfigure(0, weight=0)
        #self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        #self.labelAppTitle = customtkinter.CTkLabel(self, text="Voyage Fleet",font=customtkinter.CTkFont(size=24, weight="bold", slant="roman", family="Roboto"))
        #self.labelAppTitle.grid(row=0, column=0, sticky="nw")
        
    
        self.frames = {}
        """for frame in (LoginFrame, RegistrationFrame):
            page_name = frame.__name__
            initialized_frame = frame(self)
            print(page_name)
            self.frames[page_name] = initialized_frame
            self.frames[page_name].grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        """
        # self.holderFrame = customtkinter.CTkFrame(self, corner_radius=15, bg_color="transparent")
        # self.holderFrame.grid(row=0, column=0, sticky="ns")

        self.frames["loginFrame"] = LoginFrame(self)
        #self.frames["loginFrame"].grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        self.frames["loginFrame"].grid(row=0, column=1, sticky="")
        self.frames["registerFrame"] = RegistrationFrame(self)
        #self.frames["registerFrame"].grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        self.frames["registerFrame"].grid(row=0, column=2, sticky="")
    
        #self.show_frame("loginFrame")

        #self.hiddenFrame = customtkinter.CTkFrame(self, width=0, height=0)
        #self.hiddenFrame.grid(row=1000, column=1000)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for key_page_name in self.frames.keys():
            frame = self.frames[key_page_name]
            if key_page_name == page_name:
                frame.tkraise()

                #frame.configure(master = "root")
                continue
            #frame.configure(master = "Frame")

    def resize_background(self, width, height):
        
        self.bg_image = customtkinter.CTkImage(light_image=self.bg_loaded_light_image,
                                dark_image=self.bg_loaded_dark_image ,
                                size=(width, height))
        self.bg_image_label.configure(text="", image=self.bg_image)         

def Main():
    app = LoginPage()

    def bg_resizer(e):
        # for wraping background on resize
        if e.widget is app:
            app.resize_background(e.width, e.height)

    app.bind("<Configure>", bg_resizer)

    app.mainloop()


if __name__ == "__main__":
    Main()

# todo make login and register frame center aligned
# todo make  
