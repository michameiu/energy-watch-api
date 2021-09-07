from rest_framework.permissions import BasePermission

from client.models import ADMIN_ROLES

SAFE_METHODS = ['POST', 'HEAD', 'OPTIONS']

READ_SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAuthenticatedOrPOSTOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user and
                request.user.is_authenticated):
            return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class IsSafariNjemaCustomerCareOrAdmin(BasePermission):
    message = "Only admins or customer care agents allowed."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ADMIN_ROLES


class IsSafariNjemaCustomerCareOrAdminOrGETOnly(BasePermission):
    message = "You are not the owner or  an admin / customer care agent"

    def has_permission(self, request, view):
        if request.method in READ_SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ADMIN_ROLES


class IsSafariNjemaTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "T"


class IsOwnerTechnicianOrAdmin(BasePermission):
    message = "Not allowed to make changes to repair request"

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.role == "T":
            return obj.technician_id == request.user.id

        return obj.user.id == request.user.id or request.user.role in ADMIN_ROLES
