from rest_framework.permissions import BasePermission

class isActivated(BasePermission):
    message = "This account is not activated"
    def has_object_permission(self,request, view, object)
        return request.user.is_active