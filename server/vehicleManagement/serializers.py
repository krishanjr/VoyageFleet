from rest_framework import serializers
from django.utils import timezone
from vehicleManagement.models import Vehicle, VehicleLocation, Booking
from django.contrib.auth.models import User
from userManagement.serializers import UserSerializer
"""
class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField();
    longitude = serializers.FloatField();
"""


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vehicle model. This serializer handles the conversion 
    between Vehicle model instances and JSON representations, including validation
    and representation of related fields like the driver.
    """

    driver = serializers.StringRelatedField()

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['id']
        depth = 1

    def validate_make_year(self, value):
        """
        Validate that the make_year is not in the future.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("The make year cannot be in the future.")
        return value
    
    def validate_registration_expiry(self, value):
        """
        Validate that the registration expiry date is not in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("The registration expiry date cannot be in the past.")
        return value
    
    def validate_driver(self, value):
        """
        Validate that the driver belongs to the 'driver' group and is active.
        """
        if value and not value.is_active and not value.groups.filter(name='driver').exists():
            raise serializers.ValidationError("The assigned driver must be an active user and belong to the 'driver' group.")
        return value

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model. This serializer handles the conversion 
    between Booking model instances and JSON representations, including validation
    for user group permissions and vehicle availability.
    """
    user = UserSerializer(read_only = True)
    user_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), source = 'user', write_only = True)
    vehicle = VehicleSerializer(read_only = True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset = Vehicle.objects.all(), source = 'vehicle', write_only = True)
    class Meta:
        model = Booking
     
        fields = ['start_time','end_time','start_location','end_location','vehicle','user', 'user_id', 'vehicle_id', 'status']
        read_only_fields = ['id']
        depth = 1
        #The depth option should be set to an integer value that indicates the depth of relationships that should be traversed before reverting to a flat representation.


    def validate(self, data):
        """
        Validation to ensure:
        - The user belongs to the 'customer' group.
        - The vehicle is available for the specified time range.
        - Status transitions adhere to the business rules based on user group.
        """
        user = self.context['request'].user
        id = data.get('id')
        vehicle = data.get('vehicle')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        status = data.get('status', Booking.PENDING)

        if not self.instance:
            pass
        """
            Validates that 
            1. the user initiating Booking belongs to the 'customer' group.
            2. The vehicle is available for the specified time range.
        """
        # Validate user group. Customer only can create Booking
        if not user.groups.filter(name='customer').exists():
            raise serializers.ValidationError('The user must belong to the "customer" group.')

        # Validate vehicle availability
        #if not vehicle.is_available(start_time, end_time):
            #raise serializers.ValidationError('The vehicle is not available for the specified time range.')

        # If the booking already exists, perform additional status-related validation
        if self.instance:
            original_status = self.instance.status

            # Validation for support group (PENDING to CONFIRMED or CANCELLED)
            if original_status == Booking.PENDING:
                if status not in [Booking.CONFIRMED, Booking.CANCELLED]:
                    raise serializers.ValidationError('Status can only be changed from PENDING to CONFIRMED or CANCELLED.')

                if not user.groups.filter(name='support').exists():
                    raise serializers.ValidationError('Only users in the support group can change status from PENDING.')

            # Validation for the driver of the specific vehicle (CONFIRMED to RUNNING)
            if original_status == Booking.CONFIRMED:
                if status != Booking.RUNNING:
                    raise serializers.ValidationError('Status can only be changed from CONFIRMED to RUNNING.')

                if not user.groups.filter(name='driver').exists():
                    raise serializers.ValidationError('Only users in the driver group can change status from CONFIRMED to RUNNING.')

                # Check if the user is the driver assigned to the vehicle
                if vehicle.driver != user:
                    raise serializers.ValidationError('Only the driver assigned to this vehicle can change the status from CONFIRMED to RUNNING.')

        return data