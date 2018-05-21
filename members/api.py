import uuid
import json
import requests

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.fields import CharField
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_jwt.compat import PasswordField
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


from users.models import User
from users.permissions import isOwner

from members import permissions
from members.models import *
from members.permissions import IsMFSInactive
from members.serializers import UserMembershipSerializer


class UserMembershipView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    queryset = User.objects.all()
    model = User
    serializer_class = UserMembershipSerializer
    lookup_field = 'email'


class RequestMFS(GenericAPIView):
    permission_classes = [IsMFSInactive]
    serializer_class = type('', (Serializer,), {'password': PasswordField(
        required=True, max_length=50, allow_blank=False, allow_null=False)})

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
    serializer_class = type('', (Serializer,), {'token': CharField(
        required=True, max_length=50, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data['token']

        # TODO: Send activation token to MFS, activate user locally and populate relevant fields and relay response
        # to user

        return Response({'status': 'success', 'message': 'Successfully activated MFS account'}, status=200)


class UserMFSStatus(GenericAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):
        # request mfs details
        # import pdb 
        # pdb.set_trace()
        user = request.user

        header = {"Authorization": "Bearer TestAPIKey"}
        payload = {
            "Request": {
                "mobile_number": user.phone_number,
            }
        }

        r = requests.post("https://mobiloantest.mfs.co.ke/api/v1/status",
                          data=json.dumps(payload), headers=header)

        try:
            if(r.status_code == 200):
                response = r.json()
                if(response["Response"]['status_code'] == 200):
                    return JsonResponse(response)
                else:
                    return JsonResponse( {
                        'status': 'Not found',
                        'message': "unable to get user information"
                    }, status = 404)     
        except:
            raise("cannot creat MFS account")
        return HttpResponse("")

