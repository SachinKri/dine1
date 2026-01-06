from rest_framework.permissions import BasePermission

class IsInternalService(BasePermission):
    """
    Allows access only to internal service requests
    """

    def has_permission(self, request, view):
        internal_key = request.headers.get("X-INTERNAL-KEY")
        return internal_key == "DINSTREAM_INTERNAL"