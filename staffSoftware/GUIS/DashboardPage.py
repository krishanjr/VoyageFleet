import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar

import sys
sys.path.append('.')

import sideBar
import registerStaffPage
import vehiclePage
import BookingViewPage

from bridgeAPIPages import loginStaff

class DashboardPage(customtkinter.CTk):
    """Class representing the login GUI."""
    width = 1280          # width
    height = 768         # height
    bg_light_image = "Image/Background_gradient.jpg"
    bg_dark_image = "Image/Background_gradient.jpg"
    def __init__(self, userDetail):
        super().__init__()
        self.userDetail = userDetail
        
        self.title("Voyage Fleet")
        self.geometry(f"{self.width}x{self.height}+0+0")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Place Side bar
        self.sidebarFrame = sideBar.SidebarFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(10, weight=1)

        
        # self.mainframe = registerStaffPage.RegistrationFrame(self)
        self.change_frame("ViewBookingsFrame")

    def get_staff_credential(self):
        return get_staff_credential()

    def change_frame(self, frame_name):
        width = 1280-140
        match frame_name:
            case "ViewBookingsFrame":
                self.mainframe = BookingViewPage.ViewBookingsFrame(self, width = width)
            case "VehicleListForm":
                self.mainframe = vehiclePage.VehicleListForm(self, width = width)
            case "VechicleRegistrationFrame":
                self.mainframe = vehiclePage.VechicleRegistrationFrame(self, width = width)
            case "RegistrationFrame":
                self.mainframe = registerStaffPage.RegistrationFrame(self, width = width)

                
        self.mainframe.grid(row=0, column=1, columnspan=3, rowspan=4, sticky="nsew")
        self.mainframe.grid_rowconfigure(10, weight=1)        

staff_credential = None
staff_detail = None
def get_staff_detail():
    global staff_detail
    if staff_detail == None:
        # staff is not logged in 
        # open login page
        gotoLogin()
    return staff_detail

def get_staff_credential():
    global staff_credential
    if staff_credential == None:
        # staff is not logged in 
        # open login page
        gotoLogin()    
    return staff_credential

def gotoLogin():
    import LoginPage
    LoginPage.Main()
    #self.parentPage.destroy()   
    exit() 



def Main(username, password):
    # login and store credentials
    credential = (username, password)
    login_resp = loginStaff(credential=credential)
    if login_resp.status_code != 200:
        #login failed
        gotoLogin()
    global staff_detail
    global staff_credential
    staff_credential = credential
    staff_detail = login_resp.json_data
    app = DashboardPage(get_staff_detail())
    app.mainloop()

if __name__ == "__main__":
    Main("admin","SudinKri")