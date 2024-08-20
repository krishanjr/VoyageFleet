from rest_framework import permissions
from django.contrib.auth.models import  User
from .models import Customer, Driver, SupportStaff
"""
class IsCustomerOrReadOnly(permissions.BasePermission):

    # Permission to only allow only Customer to edit own record.


    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions of their own record are only allowed to the Customer.
        return obj.owner == request.user

"""
class IsAdminOrSupportStaff(permissions.BasePermission):
    """
    Custom permission to only allow admin and support staff to access the data.
    """
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.groups.filter(name='support_staff').exists()

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to allow only customers to view and update their own record.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='customer').exists()

class IsSelfCustomer(permissions.BasePermission):
    """
    Custom permission to allow only customers to view and update their own record.
    """
    # for object level permissions
    def has_object_permission(self, request, view, customer_id):
        return Customer.objects.get(id=customer_id.id).user.id == request.user.id