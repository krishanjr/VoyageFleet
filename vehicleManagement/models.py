from django.db import models
from django.forms import JSONField
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from userManagement.models import Driver 

class Vehicle(models.Model):
    """
    The Vehicle model represents a single vehicle within the fleet. 
    It stores detailed information about the vehicle's characteristics, 
    such as make, model, year, and other important attributes related 
    to its operation and availability within the VoyageFleet system.
    """
    
    # DEfine Vehicle Types
    SEDAN = 'SE'
    SUV = 'SU'
    MOTORCYCLE = 'MO'
    TRUCK = 'TR'
    VAN = 'VA'
    BUS = 'BU'
    OTHER = 'OT'

    VEHICLE_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (MOTORCYCLE, 'Motorcycle'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
        (BUS, 'Bus'),
        (OTHER, 'Other'),
    ]
    """
    Different Vechicle type within VoyageFleet system. Since vehicle types
    are not dynamic within our system so storing it as list of tuple.
    """

    # Define Fuel Types
    PETROL = 'PE'
    DIESEL = 'DI'
    ELECTRIC = 'EL'
    HYBRID = 'HY'
    CNG = 'CN'
    LPG = 'LP'

    FUEL_TYPES = [
        (PETROL, 'Petrol'),
        (DIESEL, 'Diesel'),
        (ELECTRIC, 'Electric'),
        (HYBRID, 'Hybrid'),
        (CNG, 'CNG'),
        (LPG, 'LPG'),
    ]
    """
    Fuel Type used by particular Vehicle. Since fuel types are limited and 
    not dynamic in nature so storing it as list of tuple.
    """

    # Define Transmission Type
    MANUAL = 'M'
    AUTOMATIC = 'A'
    SEMIAUTOMATIC = 'S'

    TRANSMISSION_TYPES = [
        (MANUAL, 'Manual'),
        (AUTOMATIC, 'Automatic'),
        (SEMIAUTOMATIC, 'Semi Automatic'),
    ]
    """
    Transmission Type used by particular Vehicle. Since Transmission types are limited and 
    not dynamic in nature so storing it as list of tuple.
    """

    # define Maintenance Statuses
    ACTIVE = 'A'
    IN_MAINTENANCE = 'I'
    OUT_OF_SERVICE = 'O'
    RETIRED = 'R' 

    MAINTENANCE_STATUSES = [
        (ACTIVE, 'Active'),
        (IN_MAINTENANCE, 'In Maintenance'),
        (OUT_OF_SERVICE, 'Out of Service'),
        (RETIRED, 'Retired'),
    ]
    """
    A list of tuples representing the possible maintenance statuses for a vehicle.
    
    - 'ACTIVE': The vehicle is in good condition and available for use.
    - 'IN_MAINTENANCE': The vehicle is currently undergoing maintenance or repairs.
    - 'OUT_OF_SERVICE': The vehicle is not operational due to serious issues.
    - 'RETIRED': The vehicle is no longer in active service or has been decommissioned.
    """

    id = models.BigAutoField(primary_key=True)
    """Auto-incrementing primary key."""

    #active = models.BooleanField(default=True)
    #"""is Vehicle Active and can be used within Voyage Fleet system. Defaults to True"""
    #This is already used in Maintenance status

    #deleted = models.BooleanField(default=False)
    #"""is Vehicle deleted from Voyage Fleet system. Since we are using particular Vehicle in Booking so marking it as deleted for history"""
    #Since we already implemented Maintenance status. Simply setting Maintenance status to Retired is same as deleted

    license_plate_number = models.CharField(max_length=16, unique=True)
    """Unique identifier for the vehicle, a unique code for the vehicle typically the registration number. eg: Ba Dha 029 Cha 1343"""

    make = models.CharField(max_length=50)
    """Manufacturer of the vehicle. eg: Suzuki"""

    model = models.CharField(max_length=50)
    """Specific model of the vehicle. eg: Swift"""

    makeyear = models.IntegerField()
    """Manufacturing year. eg: 2011"""

    color = models.CharField(max_length=30)
    """Vehicle's color. eg: Silver"""

    vehicle_type = models.CharField(max_length=2, choices=VEHICLE_TYPES)
    """The type of the vehicle, chosen from predefined options(VEHICLE_TYPES)."""

    seating_capacity = models.IntegerField()
    """Number of seats in the vehicle including Driver. eg: 5"""

    fuel_type = models.CharField(max_length=2, choices=FUEL_TYPES)
    """The type of fuel the vehicle uses, chosen from predefined options(FUEL_TYPES)."""

    transmission_type = models.CharField(max_length=1, choices=TRANSMISSION_TYPES)
    """The type of transmission, chosen from predefined options(TRANSMISSION_TYPES)."""

    def __str__(self):
        return f'{self.make} {self.model} ({self.license_plate_number})'
    #current_odometer_reading = models.DecimalField(max_digits=10, decimal_places=2)
    #"""Current mileage of the vehicle."""

    maintenance_status = models.CharField(
        max_length=1, 
        choices=MAINTENANCE_STATUSES, 
        default=ACTIVE
    )
    """Current maintenance status of the vehicle. chosen from predefined options(MAINTENANCE_STATUSES)."""

    registration_expiry_date = models.DateField()
    """The date when the vehicle’s registration expires."""

    #availability_status = models.CharField(max_length=20, default='Available')
    #"""Whether the vehicle is available, booked, or out of service."""
    # This is now given by function is_available
    
    driver_id = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'groups__name': 'staff_driver'},
        related_name='vehicles'
    )
    """Foreign key referencing the User model, representing the driver assigned to the vehicle, restricted to users in the 'staff_driver' group."""

    
    created_at = models.DateTimeField(auto_now_add=True)
    """When was this vehicle entry made"""
    updated_at = models.DateTimeField(auto_now=True)
    """When was this vehicle information updated"""
    
    def is_available(self, start_time, end_time):
        """
        Checks if the vehicle is available for booking within a given time range.
        
        The vehicle is considered available if it is not currently booked within the 
        given time range, its maintenance status is 'Active' and registration is not expired.
        
        Args:
            start_time (datetime): The start time of the requested booking period.
            end_time (datetime): The end time of the requested booking period.
        
        Returns:
            bool: True if the vehicle is available, False otherwise.
        """
        if self.maintenance_status not in ['ACTIVE']:
            return False
        
        # Check if the vehicle's registration is expired
        if self.registration_expiry_date < timezone.now().date():
            return False
        
        overlapping_bookings = Booking.objects.filter(
            vehicle=self,
            status__in=[Booking.PENDING, Booking.CONFIRMED, Booking.RUNNING],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        return not overlapping_bookings.exists()

    #driver_id = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    #"""Foreign key linking to a Driver model, representing the driver assigned to the vehicle."""
    def clean(self):
        """
        Validate that the assigned driver belongs to the 'staff_driver' group.
        """
        if self.driver_id and not self.driver_id.groups.filter(name='staff_driver').exists():
            raise ValidationError('The selected driver must be a member of the "staff_driver" group.')


class Location:
    """
    The Location class encapsulates geographic coordinates (latitude and longitude).
    It is used to represent the start and end locations in bookings and VehicleLocation
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f'Location ({self.latitude}, {self.longitude})'

    def to_dict(self):
        """
        Converts the location instance to a dictionary format.
        """
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Location instance from a dictionary.
        """
        return Location(latitude=data['latitude'], longitude=data['longitude'])

class LocationCreator:
  
    def __init__(self, field):
        self.field = field
  
    def __get__(self, obj):
        if obj is None:
            return self
      
        return obj.__dict__(self.field.name)
  
    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.convert_input(value)

    def convert_input(self, value):
        if value is None:
            return None
        
        if isinstance(value, Location):
            return value
        else:
            return Location(**value)
        
class LocationField(models.JSONField):

    def from_db_value(self, value, expression, connection):
        # decode the database value into an instance of our class(Location)
        db_val = super().from_db_value(value, expression, connection)

        if db_val is None:
            return db_val
        
        return Location(**db_val)
    
    def get_prep_value(self, value):
        # convert our class(Location) into a python dictionary and then it calls 
        # JSONField’s super implementation, which will simply encode 
        # the dictionary as a string.
        dict_value = value.to_dict()
        prep_value = super().get_prep_value(dict_value)
        return prep_value
    
    def contribute_to_class(self, cls, name, private_only=False):
        # https://lazypython.blogspot.com/2008/11/django-models-digging-little-deeper.html
        super().contribute_to_class(cls, name, private_only=private_only)
        setattr(cls, self.name, LocationCreator(self))

class Booking(models.Model):
    """
    The Booking model stores information about vehicle bookings, including
    the user who made the booking, the vehicle being booked, and the start
    and end times of the booking. Only users from the 'customer' group are allowed 
    to make a booking.
    """
    # Define booking status choices
    PENDING = 'P'
    CONFIRMED = 'C'
    CANCELLED = 'X'
    RUNNING = 'R'
    COMPLETED = 'D'

    BOOKING_STATUSES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
    ]
    """
    A list of tuples representing the booking statuses for a vehicle.
    
    - 'PENDING': The Booking is initiated by "Customer" yet to be reviewed by "Support" staff.
    - 'CONFIRMED': The Booking is Confirmed by "Support" staff.
    - 'CANCELLED': The Booking is Cancelled by "Support" staff.
    - 'RUNNING': The Booking is current Running.
    - 'COMPLETED': The Booking is Completed.
    """

    id = models.BigAutoField(primary_key=True)
    """Auto-incrementing primary key."""

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    """Foreign key referencing the vehicle being booked."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'customer'}
    )
    """Foreign key referencing the user who made the booking, restricted to the 'customer' group."""

    status = models.CharField(
        max_length=1,
        choices=BOOKING_STATUSES,
        default=PENDING
    )
    """The status of the booking, indicating its current state."""

    start_time = models.DateTimeField()
    """The start time of the booking."""

    end_time = models.DateTimeField()
    """The end time of the booking."""

    #start_location = LocationField()
    start_location = models.TextField()
    """The starting location of the booking."""

    #end_location = LocationField()
    end_location = models.TextField()
    """The ending location of booking"""

    #start_location_latitude = models.FloatField()
    #"""The latitudeof the starting location of the booking."""

    #start_location_longitude = models.FloatField()
    #"""The longitude of the starting location of the booking."""

    #end_location_latitude = models.FloatField()
    #"""The latitude of the ending location of the booking."""

    #end_location_longitude = models.FloatField()
    #"""The latitude of the ending location of the booking."""

    """
    def get_start_location(self):
        #Returns the start location as a Location object.
        return Location(self.start_location_latitude, self.start_location_longitude)

    def get_end_location(self):
        #Returns the end location as a Location object.
        return Location(self.end_location_latitude, self.end_location_longitude)
    """

    def __str__(self):
        return f'Booking for {self.vehicle} by {self.user} from {self.start_time} to {self.end_time}'

    class Meta:
        ordering = ['-start_time']
        """Orders the bookings by start time in descending order."""

class VehicleLocation(models.Model):
    """
    The VehicleLocation model stores the GPS location of a vehicle at 
    specific time intervals. It records the latitude, longitude, timestamp, 
    and a reference to the vehicle, allowing tracking of the vehicle's 
    movement over time.
    """

    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    """Foreign key referencing the vehicle whose location is being tracked."""

    location = LocationField()
    """Location of vehicle"""

    #latitude = models.FloatField()
    """The latitude of the vehicle's location."""

    #longitude = models.FloatField()
    """The longitude of the vehicle's location."""

    timestamp = models.DateTimeField(default=timezone.now)
    """The exact date and time when the location was recorded."""

    """def get_location(self):
        
        #Returns the location as a Location object.
        
        return Location(self.latitude, self.longitude)"""

    def set_location(self, location):
        """
        Sets the latitude and longitude from a Location object.
        """
        self.latitude = location.latitude
        self.longitude = location.longitude

    def __str__(self):
        return f'Location of {self.vehicle} at {self.timestamp} is {self.latitude}, {self.longitude}'

    class Meta:
        ordering = ['-timestamp']
        """Orders the records by timestamp in descending order."""

