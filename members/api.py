import uuid

from rest_framework import status
from rest_framework.fields import CharField
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_jwt.compat import PasswordField

from members import permissions
from members.permissions import IsMFSInactive

class RequestMFS(GenericAPIView):
    permission_classes = [IsMFSInactive]
    serializer_class = type('', (Serializer,), {'password': PasswordField(required=True, max_length=50, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.check_password(serializer.validated_data['password']):
            return Response({
                    'status': 'Invalid operation',
                    'message': "Invalid password"
                }, status=400)

        member = request.user.member
        # TODO: Add code to register MFS account

        return Response({'status': 'success', 'message': 'Successfully created MFS account'}, status=200)


class ActivateMFS(GenericAPIView):
    permission_classes = [IsMFSInactive]
    serializer_class = type('', (Serializer,), {'token': CharField(required=True, max_length=50, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data['token']

        # TODO: Send activation token to MFS, activate user locally and populate relevant fields and relay response
        # to user

        return Response({'status': 'success', 'message': 'Successfully activated MFS account'}, status=200)