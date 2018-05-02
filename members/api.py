import uuid

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from members import permissions


class ActivateMFS(GenericAPIView):
    permission_classes = (permissions.IsMFSInactive,)

    def get(self, request, **kwargs):
        member = request.user.member
        member.is_msf_active = True
        member.msf_account = uuid.uuid4()
        member.save()
        return Response({"message": "MFS account successfully activated"})

    def post(self, request, **kwargs):
        return self.get(request, **kwargs)