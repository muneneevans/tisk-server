from rest_framework.permissions import IsAuthenticated
import users.permissions
import members.models

class IsMember(users.permissions.isActivated):
    def has_object_permission(self,request, view, object):
        allowed =  super(IsMember, self).has_object_permission(request, view, object)
        if not allowed: return allowed
        self.message = "user is not a member"
        try:
            member = request.user.member
            return True
        except:
            return False

    def has_permission(self, request, view):
        allowed = super(IsMember, self).has_permission(request, view)
        if not allowed: return allowed
        self.message = "user is not a member"
        try:
            member = request.user.member
            return True
        except:
            return False

class IsApprovedMember(IsMember):

    def has_permission(self, request, view):
        allowed = super(IsApprovedMember, self).has_permission(request, view)
        if not allowed: return allowed
        self.message = "user is not an approved member"
        return request.user.member.status == members.models.Member.APPROVED

    def has_object_permission(self, request, view, object):
        allowed = super(IsApprovedMember, self).has_object_permission(request, view, object)
        if not allowed: return allowed
        self.message = "user is not an approved member"
        return request.user.member.status == members.models.Member.APPROVED

class IsMFSInactive(IsMember):

    def has_permission(self, request, view):
        allowed = super(IsMFSInactive, self).has_permission(request, view)
        if not allowed: return allowed
        self.message = "user already has msf active"
        return  not request.user.member.is_msf_active

    def has_object_permission(self, request, view, object):
        allowed = super(IsMFSInactive, self).has_object_permission(request, view, object)
        if not allowed: return allowed
        self.message = "user already has mfs active"
        return  not request.user.member.is_msf_active