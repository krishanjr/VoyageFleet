import tkinter as tk
import customtkinter
from PIL import Image
from tkcalendar import Calendar, DateEntry

import requests

import sys
sys.path.append('.')
from bridgeAPIPages import validate_vehicle_form
import APIFunctions

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox

class VehicleListForm(customtkinter.CTkScrollableFrame):
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        super().__init__(parentPage, **kwargs)   
        self.logo_label = customtkinter.CTkLabel(self, text="View All Vehicles", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(fill="both", expand=True)
        self.vehicle_tree = ttk.Treeview(self, columns=("ID", "License Plate", "Make", "Model", "Year", "Type", "Driver"))
        self.vehicle_tree.heading("#0", text="")
        self.vehicle_tree.heading("ID", text="ID")
        self.vehicle_tree.heading("License Plate", text="License Plate")
        self.vehicle_tree.heading("Make", text="Make")
        self.vehicle_tree.heading("Model", text="Model")
        self.vehicle_tree.heading("Year", text="Year")
        self.vehicle_tree.heading("Type", text="Type")
        self.vehicle_tree.heading("Driver", text="Driver")

        self.vehicle_tree.column("#0", width=0, stretch=tk.NO)
        self.vehicle_tree.column("ID", anchor=tk.CENTER, width=40)
        self.vehicle_tree.column("License Plate", anchor=tk.CENTER, width=120)
        self.vehicle_tree.column("Make", anchor=tk.CENTER, width=120)
        self.vehicle_tree.column("Model", anchor=tk.CENTER, width=120)
        self.vehicle_tree.column("Year", anchor=tk.CENTER, width=80)
        self.vehicle_tree.column("Type", anchor=tk.CENTER, width=100)
        self.vehicle_tree.column("Driver", anchor=tk.CENTER, width=120)

        self.vehicle_tree.pack(fill="both", expand=True)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Vehicle List", command=self.fetch_vehicle_data)
        self.refresh_button.pack(pady=10)

        self.fetch_vehicle_data()

    def fetch_vehicle_data(self):
        try:
            response = APIFunctions.VehicleAPI().get_all(auth = self.parentPage.get_staff_credential())
            if response.status_code != 200:
                return messagebox.showerror('Error', response.json_data)
            vehicles = response.json_data


            for item in self.vehicle_tree.get_children():
                self.vehicle_tree.delete(item)

            for vehicle in vehicles:
                driver_name = vehicle['driver_id']['first_name'] if vehicle['driver_id'] else "Unassigned"
                self.vehicle_tree.insert("", tk.END, values=(
                    vehicle['id'],
                    vehicle['license_plate_number'],
                    vehicle['make'],
                    vehicle['model'],
                    vehicle['makeyear'],
                    vehicle['vehicle_type'],
                    driver_name
                ))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch vehicle data: {e}")

    

class VechicleRegistrationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        super().__init__(parentPage, **kwargs)        

        self.create_label_entry("License Plate Number", 0)
        self.create_label_entry("Make", 1)
        self.create_label_entry("Model", 2)
        self.create_label_entry("Make Year", 3)
        self.create_label_entry("Color", 4)

        self.vehicle_type_map = {
            "Sedan" : 'SE', 
            "SUV" : 'SU', 
            "Motorcycle" : 'MO', 
            "Truck" : 'TR', 
            "Van" : 'VA', 
            "Bus" : 'BU', 
            "Other" : 'OT'
        }
        self.create_dropdown("Vehicle Type", 5, ["Sedan", "SUV", "Motorcycle", "Truck", "Van", "Bus", "Other"])
        self.create_label_entry("Seating Capacity", 6)

        self.fuel_type_map = {
            'Petrol' : 'PE' ,
            'Diesel' : 'DI' ,
            'Electric' : 'EL' ,
            'Hybrid' : 'HY' ,
            'CNG' : 'CN' ,
            'LPG' : 'LP' 
        }
        self.create_dropdown("Fuel Type", 7, ["Petrol", "Diesel", "Electric", "Hybrid", "CNG", "LPG"])
        self.transmission_type_map = {
            "Manual" : "M", 
            "Automatic" : "A", 
            "Semi Automatic" : "S"
        }
        self.create_dropdown("Transmission Type", 8, ["Manual", "Automatic", "Semi Automatic"])

        self.maintenance_status_map = {
            "Active": "A",
            "In Maintenance": "I", 
            "Out of Service": "O", 
            "Retired": "R"
        }
        self.create_dropdown("Maintenance Status", 9, ["Active", "In Maintenance", "Out of Service", "Retired"])
        
        self.create_date_entry("Registration Expiry Date", 10)
        #self.create_label_entry("Driver ID", 11)
        self.create_driver_dropdown(11)

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text="Add new Vehicle", command=self.register_event)
        self.submit_button.grid(row=12, column=0, columnspan=2, pady=20)    

    def create_date_entry(self, label_text, row):
        label = ctk.CTkLabel(self, text = label_text)
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        entry = DateEntry(self)
        entry.grid(row=row, column=1, padx=10, pady=10)
        setattr(self, f"{label_text.replace(' ', '_').lower()}_entry", entry)

    def create_label_entry(self, label_text, row):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=10, pady=10)
        setattr(self, f"{label_text.replace(' ', '_').lower()}_entry", entry)

    def create_dropdown(self, label_text, row, options):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        dropdown = ctk.CTkComboBox(self, values=options)
        dropdown.grid(row=row, column=1, padx=10, pady=10)
        setattr(self, f"{label_text.replace(' ', '_').lower()}_dropdown", dropdown)
            
    def create_driver_dropdown(self, row):
        label = ctk.CTkLabel(self, text="Driver Name")
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        drivers = self.fetch_drivers()
        self.driver_map = {f"{driver['first_name']} {driver['last_name']}": driver['id'] for driver in drivers}
        dropdown = ctk.CTkComboBox(self, values=list(self.driver_map.keys()))
        dropdown.grid(row=row, column=1, padx=10, pady=10)
        self.driver_dropdown = dropdown

    def register_event(self):
        """Register Button is pressed"""
        try:
            


            inputs = {
                "license_plate_number": self.license_plate_number_entry.get(),
                "make": self.make_entry.get(),
                "model": self.model_entry.get(),
                "makeyear": int(self.make_year_entry.get()),
                "color": self.color_entry.get(),
                "vehicle_type": self.vehicle_type_map[self.vehicle_type_dropdown.get()],
                "seating_capacity": int(self.seating_capacity_entry.get()),
                "fuel_type": self.fuel_type_map[self.fuel_type_dropdown.get()],
                "transmission_type": self.transmission_type_map[self.transmission_type_dropdown.get()],
                "maintenance_status": self.maintenance_status_map[self.maintenance_status_dropdown.get()],
                "registration_expiry_date": str(self.registration_expiry_date_entry.get_date()),
                "driver_id": self.driver_map[self.driver_dropdown.get()]
            }
        except(ValueError):
            return messagebox.showerror("Error", "Please validate your input")
        #validated_inputs = validate_register_staff_form(inputs)
        # todo add validation here
        if not isinstance(inputs, dict):
            return messagebox.showerror('Error',inputs)
        #input is validated now sending to server
        api = APIFunctions.VehicleAPI()
        response = api.create(inputs, auth=self.parentPage.get_staff_credential())
        print(inputs)      
        if response.status_code == 201:
            # successfully created
            return messagebox.showinfo('Vehicle Created', "Vehicle of Registration Number" + self.license_plate_number_entry.get() + " created Successfully")


        else:
            # todo add errorFrame to show error. Best for UI to show error
            return messagebox.showerror('Error', response.json_data)


    def fetch_drivers(self):
        response = requests.get("http://127.0.0.1:8000/userMgmt/driver/unassignedDriver/")
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror('Error', "Failed to fetch drivers.")
            return []