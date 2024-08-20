from django.db import models
from django.contrib.auth.models import User

USER_GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]

class Customer(models.Model):
    """
    Model to store customer data.
    """

    # Links the customer to a Django User model using a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    # Stores the customer's phone number, ensuring it is unique
    phone_number = models.CharField(max_length=15, unique=True)
    
    # Stores the customer's address
    address = models.TextField()
    
    # Stores the customer's date of birth
    date_of_birth = models.DateField()
    
    # Stores the customer's gender with choices (Male, Female, Other)
    gender = models.CharField(max_length=1, choices=USER_GENDER_CHOICES)


class Driver(models.Model):
    """
    Model to store driver data.
    """

    # Links the driver to a Django User model using a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    
    # Stores the driver's license number, ensuring it is unique
    license_number = models.CharField(max_length=20, unique=True)
    
    # Stores the driver's phone number, ensuring it is unique
    phone_number = models.CharField(max_length=15, unique=True)
    
    # Stores the driver's address
    address = models.TextField()
    
    # Stores the driver's date of birth
    date_of_birth = models.DateField()
    
    # Stores the driver's gender with choices (Male, Female, Other)
    gender = models.CharField(max_length=10, choices=USER_GENDER_CHOICES)
    
    # Stores the date when the driver's license expires
    license_expiry_date = models.DateField()

class SupportStaff(models.Model):
    """
    Model to store support staff information.
    """

    # Links the support staff to a Django User model using a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='support_staff_profile')
    
    # Stores the support staff's phone number, ensuring it is unique
    phone_number = models.CharField(max_length=15, unique=True)
    
    # Stores the support staff's address
    address = models.TextField()
    
    # Stores the support staff's date of birth
    date_of_birth = models.DateField()
    
    # Stores the support staff's gender with choices (Male, Female, Other)
    gender = models.CharField(max_length=10, choices=USER_GENDER_CHOICES)
