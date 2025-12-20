from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    """
    Base class for role-based permissions
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )
    
class IsAdminRole(BaseRolePermission):
    allowed_roles = ["admin"]


class IsCustomerRole(BaseRolePermission):
    allowed_roles = ["customer"]


class IsRestaurantAdminRole(BaseRolePermission):
    allowed_roles = ["restaurant_admin"]


class IsDeliveryPartnerRole(BaseRolePermission):
    allowed_roles = ["delivery_partner"]