from rest_framework.permissions import BasePermission

class isActivated(BasePermission):
    message = "This account is not activated"
    def has_object_permission(self,request, view, object):
        return request.user.is_active


class isOwner(BasePermission):
    message = "THis account is does not have right to view"

    def has_object_permission(self, request, view, object):
        return request.user.id == object.id