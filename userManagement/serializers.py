from django.contrib.auth.models import (
    Group, 
    User
)

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from django.contrib.auth import authenticate


from .models import (
    USER_GENDER_CHOICES, 
    Customer, 
    Driver, 
    SupportStaff
)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True, required=False)
    class Meta:
        model = User
        # depth = 1
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                  'password','is_superuser', 'is_staff', 'groups')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("Creating New User")
        # Create a new user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user # super().create(validated_data)
    

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new customer.
    This will create a user and a customer profile, and assign the user to the 'customer' group.
    """
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['url', 'user', 'phone_number', 'address', 'date_of_birth', 'gender']
        read_only_fields = ("id", "pub_id")

    def create(self, validated_data):
        validated_user_data = validated_data.pop('user')
        print("Creating New Customer")
        user = User.objects.create_user(
            username=validated_user_data['username'],
            email=validated_user_data['email'],
            first_name=validated_user_data['first_name'],
            last_name=validated_user_data['last_name']
        )
        user.set_password(validated_user_data['password'])
        user.save()

        # Assign the user to the 'customer' group
        customer_group, created = Group.objects.get_or_create(name='customer')
        user.groups.add(customer_group)

        # Extract customer-related data
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        date_of_birth = validated_data.pop('date_of_birth')
        gender = validated_data.pop('gender')
        
        # Create a customer profile
        customer = Customer.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
            gender=gender
        )
        return customer # super().create(validated_data)

class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new Driver.
    This will create a user and a Driver profile, and assign the user to the 'staff_driver' group.
    """
    user = UserSerializer()
    class Meta:
        model = Driver
        fields = ['url', 'user', 'phone_number', 'address', 'date_of_birth', 'gender', 'license_number', 'license_expiry_date']
        read_only_fields = ("id", "pub_id")

    def create(self, validated_data):
        validated_user_data = validated_data.pop('user')
        print("Creating New Driver User")
        user = User.objects.create_user(
            username=validated_user_data['username'],
            email=validated_user_data['email'],
            first_name=validated_user_data['first_name'],
            last_name=validated_user_data['last_name']
        )
        user.set_password(validated_user_data['password'])
        user.save()

        # Assign the user to the 'staff_driver' group
        driver_group, created = Group.objects.get_or_create(name='staff_driver')
        user.groups.add(driver_group)

        # Extract driver-related data
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        date_of_birth = validated_data.pop('date_of_birth')
        gender = validated_data.pop('gender')
        license_number = validated_data.pop('license_number')
        license_expiry_date = validated_data.pop('license_expiry_date')

        
        # Create a driver profile
        driver = Driver.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
            gender=gender,
            license_number=license_number,
            license_expiry_date=license_expiry_date
        )
        return driver 

class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new Staff.
    This will create a user and a Staff profile, and assign the user to the 'staff_support' group.
    """
    user = UserSerializer()
    class Meta:
        model = SupportStaff
        fields = ['url', 'user', 'phone_number', 'address', 'date_of_birth', 'gender']
        read_only_fields = ("id", "pub_id")

    def create(self, validated_data):
        validated_user_data = validated_data.pop('user')
        print("Creating New Support Staff")
        user = User.objects.create_user(
            username=validated_user_data['username'],
            email=validated_user_data['email'],
            first_name=validated_user_data['first_name'],
            last_name=validated_user_data['last_name']
        )
        user.set_password(validated_user_data['password'])
        user.save()

        # Assign the user to the 'staff_support' group
        staff_group, created = Group.objects.get_or_create(name='staff_support')
        user.groups.add(staff_group)

        # Extract Staff-related data
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        date_of_birth = validated_data.pop('date_of_birth')
        gender = validated_data.pop('gender')
        
        # Create a Staff profile
        staff = SupportStaff.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
            gender=gender
        )
        return staff



class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, data):
        # Take username and password from request
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

#print(repr(CustomerSerializer()))