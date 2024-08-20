import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkcalendar import Calendar, DateEntry

import sys
sys.path.append('.')
from bridgeAPIPages import validate_register_staff_form, validate_register_driver_form
import APIFunctions



class BookingRegistrationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        super().__init__(parentPage, **kwargs)    

        # Vehicle Selection Label and ComboBox
        self.vehicle_label = customtkinter.CTkLabel(self, text="Select Vehicle:")
        self.vehicle_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.vehicle_combo = customtkinter.CTkComboBox(self, values=[])
        self.vehicle_combo.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        # Start Location Label and Entry
        self.start_location_label = customtkinter.CTkLabel(self, text="Start Location:")
        self.start_location_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.start_location_entry = customtkinter.CTkEntry(self)
        self.start_location_entry.grid(row=1, column=1, pady=10, padx=10, sticky="e")

        # End Location Label and Entry
        self.end_location_label = customtkinter.CTkLabel(self, text="End Location:")
        self.end_location_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.end_location_entry = customtkinter.CTkEntry(self)
        self.end_location_entry.grid(row=2, column=1, pady=10, padx=10, sticky="e")

        # Start Time Label and Entry
        self.start_time_label = customtkinter.CTkLabel(self, text="Start Time (YYYY-MM-DD HH:MM):")
        self.start_time_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.start_time_entry = customtkinter.CTkEntry(self)
        self.start_time_entry.grid(row=3, column=1, pady=10, padx=10, sticky="e")

        # End Time Label and Entry
        self.end_time_label = customtkinter.CTkLabel(self, text="End Time (YYYY-MM-DD HH:MM):")
        self.end_time_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        self.end_time_entry = customtkinter.CTkEntry(self)
        self.end_time_entry.grid(row=4, column=1, pady=10, padx=10, sticky="e")

        # Button to submit booking
        self.submit_button = customtkinter.CTkButton(self, text="Submit Booking", command=self.submit_booking)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Fetch vehicle list from the backend
        self.fetch_vehicles()

    def fetch_vehicles(self):
        try:
            response = APIFunctions.VehicleAPI().get_all(auth = self.parentPage.get_staff_credential())
            if response.status_code != 200:
                return messagebox.showerror('Error', response.json_data)
            vehicles = response.json_data


            vehicle_options = [f"{vehicle['make']} {vehicle['model']} ({vehicle['license_plate_number']})" for vehicle in vehicles]
            self.vehicle_id_options = {
                f"{vehicle['make']} {vehicle['model']} ({vehicle['license_plate_number']})" : vehicle['id'] for vehicle in vehicles
            }
            self.vehicle_combo.configure(values=vehicle_options)

        except:
            messagebox.showerror("Error", f"Failed to fetch vehicle data")

    def submit_booking(self):
        """
        Submits the booking data to the backend.
        """
        vehicle_selection = self.vehicle_id_options[self.vehicle_combo.get()]
        start_location = self.start_location_entry.get()
        end_location = self.end_location_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        try:
            # Validate input fields
            if not vehicle_selection or not start_location or not end_location or not start_time or not end_time:
                messagebox.showerror("Error", "All fields are required.")
                return


            # Prepare data for POST request
            booking_data = {
                "vehicle": int(vehicle_selection),
                "start_location": start_location,
                "end_location": end_location,
                "start_time": start_time,
                "end_time": end_time,
                "user": int(self.parentPage.userDetail["user"]["id"])
            }
            print(booking_data)
            # Make POST request to create the booking
            
            api = APIFunctions.BookingAPI()
            response = api.create(booking_data, auth=("sidhartha", "password"))
            print(response)      
            if response.status_code == 201:
                messagebox.showinfo("Success", "Booking created successfully!")
                return
            messagebox.showerror("Error", response.json_data)
            
        except:
            messagebox.showerror("Error", "Error creating Booking ")





class ViewBookingsFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parentPage, **kwargs):
        self.parentPage = parentPage 
        super().__init__(parentPage, **kwargs)    


        self.logo_label = customtkinter.CTkLabel(self, text="View All Bookings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(fill="both", expand=True)
        # Create a frame for the table
        self.table_frame = customtkinter.CTkFrame(self)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create the Treeview for displaying booking data
        columns = ("vehicle", "start_location", "end_location", "start_time", "end_time", "status")
        self.bookings_table = tk.ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.bookings_table.pack(fill="both", expand=True)

        # Define table headers
        self.bookings_table.heading("vehicle", text="Vehicle")
        self.bookings_table.heading("start_location", text="Start Location")
        self.bookings_table.heading("end_location", text="End Location")
        self.bookings_table.heading("start_time", text="Start Time")
        self.bookings_table.heading("end_time", text="End Time")
        self.bookings_table.heading("status", text="Status")

        # Define column widths
        self.bookings_table.column("vehicle", width=150)
        self.bookings_table.column("start_location", width=100)
        self.bookings_table.column("end_location", width=100)
        self.bookings_table.column("start_time", width=150)
        self.bookings_table.column("end_time", width=150)
        self.bookings_table.column("status", width=100)

        # Fetch and display bookings
        self.fetch_bookings()

    def fetch_bookings(self):
        """
        Fetches the list of bookings from the backend and populates the table.
        """
        response = APIFunctions.BookingAPI().get_all(auth = self.parentPage.get_staff_credential())
        if response.status_code != 200:
            return messagebox.showerror('Error', response.json_data)

        bookings = response.json_data

        # Clear existing rows
        for row in self.bookings_table.get_children():
            self.bookings_table.delete(row)

        # Insert bookings into the table
        for booking in bookings:
            vehicle_info = f"{booking['vehicle']['make']} {booking['vehicle']['model']} ({booking['vehicle']['license_plate_number']})"
            self.bookings_table.insert("", "end", values=(
                vehicle_info,
                booking["start_location"],
                booking["end_location"],
                booking["start_time"],
                booking["end_time"],
                booking["status"]
            ))

