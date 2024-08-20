import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar

import sys
sys.path.append('.')

import sideBar
#import vehiclePage
import BookingViewPage
from bridgeAPIPages import loginCustomer

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
        self.change_frame("ViewCustomerBookingsFrame")
        
    def get_customer_credential(self):
        return get_customer_credential()

    def change_frame(self, frame_name):
        width = 1280-140
        match frame_name:
            case "BookingRegistrationFrame":
                self.mainframe = BookingViewPage.BookingRegistrationFrame(self, width = width)
            case "ViewCustomerBookingsFrame":
                self.mainframe = BookingViewPage.ViewCustomerBookingsFrame(self, width = width)

                
        self.mainframe.grid(row=0, column=1, columnspan=3, rowspan=4, sticky="nsew")
        self.mainframe.grid_rowconfigure(10, weight=1)        

customer_credential = None
customer_detail = None
def get_customer_detail():
    global customer_detail
    if customer_detail == None:
        # Customer is not logged in 
        # open login page
        gotoLogin()
    return customer_detail

def get_customer_credential():
    global customer_credential
    if customer_credential == None:
        # Customer is not logged in 
        # open login page
        gotoLogin()    
    return customer_credential

def gotoLogin():
    import LoginPage
    LoginPage.Main()
    #self.parentPage.destroy()   
    exit() 



def Main(username, password):
    # login and store credentials
    credential = (username, password)
    login_resp = loginCustomer(credential=credential)
    if login_resp.status_code != 200:
        #login failed
        gotoLogin()
    global customer_detail
    global customer_credential
    customer_credential = credential
    customer_detail = login_resp.json_data
    print(get_customer_detail())
    app = DashboardPage(get_customer_detail())
    app.mainloop()

if __name__ == "__main__":
    Main("sidhartha","password")