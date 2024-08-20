from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework import generics

from userManagement.permissions import (
    IsAdminOrSupportStaff, 
    IsCustomer, 
    IsSelfCustomer
)

from userManagement.models import Customer, Driver, SupportStaff
from userManagement.serializers import (
    GroupSerializer, 
    UserSerializer , 
    CustomerSerializer, 
    DriverSerializer, 
    StaffSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAdminOrSupportStaff]

class CustomerLoginView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer

    def get_object(self):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        return customer

class SupportLoginView(generics.RetrieveAPIView):
    serializer_class = StaffSerializer

    def get_object(self):
        admin_user = User.objects.get(username="admin")

        SupportStaff.objects.get_or_create(
            user=admin_user,
            phone_number="9861332944",
            address="Banepa, Nepal",
            date_of_birth="2003-03-07",
            gender="F"
        )
        user = self.request.user
        staff = SupportStaff.objects.get(user=user)
        return staff

class DriverLoginView(generics.RetrieveAPIView):
    serializer_class = StaffSerializer

    def get_object(self):
        user = self.request.user
        driver = Driver.objects.get(user=user)
        return driver

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customer to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    #permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            # let only customer to change his/her information
            self.permission_classes = [permissions.IsAuthenticated, IsCustomer, IsSelfCustomer]
        elif self.action == 'list':
            # let admin, support staff only view all customer's data
            self.permission_classes = [permissions.IsAuthenticated, IsAdminOrSupportStaff]
        elif self.action == 'create':
            # let Anynomous be new customer
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super(CustomerViewSet, self).get_permissions()
    
# todo add permission to Driver viewset and staff viewset
class DriverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customer to be viewed or edited.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    #permission_classes = [IsAdminOrSupportStaff]

class UnassignedDriverListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='staff_driver').exclude(vehicles__isnull=False)
    serializer_class = UserSerializer

class StaffViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customer to be viewed or edited.
    """
    queryset = SupportStaff.objects.all()
    serializer_class = StaffSerializer
    #permission_classes = [IsAdminOrSupportStaff]