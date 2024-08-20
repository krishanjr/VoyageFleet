import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar, DateEntry


import sys
sys.path.append('.')
from bridgeAPIPages import loginStaff
import APIFunctions


def openDashboard(username, password):
    import DashboardPage
    DashboardPage.Main()
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
        login_resp = loginStaff(credential=credential)
        print(login_resp)
        if login_resp.status_code != 200:
            #login failed
            # todo add errorFrame to show error. Best for UI to show error
            return messagebox.showerror('Error','Incorrect Username or Password')
        gotoDashboard(self.username_input.get(), self.password_input.get())

        
def gotoDashboard(username, password):
    import DashboardPage
    DashboardPage.Main(username, password)
    #self.parentPage.destroy()   
    exit()

class LoginPage(customtkinter.CTk):
    """Class representing the login GUI."""
    width = 1280          # width
    height = 768         # height
    bg_light_image = "Image/Background_gradient.jpg"
    bg_dark_image = "Image/Background_gradient_dark.jpg"
    def __init__(self):
        super().__init__()

        self.title("Staff Login")
        self.geometry(f"{self.width}x{self.height}+0+0")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
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

        self.frames["loginFrame"] = LoginFrame(self)
        self.frames["loginFrame"].grid(row=1, column=1, sticky="ns", padx=100, pady=20)



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
