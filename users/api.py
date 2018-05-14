from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.fields import EmailField, CharField
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_jwt.compat import PasswordField

from members.permissions import IsMFSInactive
from .permissions import isOwner
from .serializers import *


class CreateUser(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    model = User
    serializer_class = UserCreateSerializer
    queryset = ''

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserInlineSerializer
        return UserCreateSerializer

class RetrieveUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    queryset = User.objects.all()
    model = User
    serializer_class = UserInlineSerializer
    lookup_field = 'email'


class ActivateUser(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = type('', (Serializer,),{'token': CharField(required=True, max_length=50, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = get_object_or_404(ActivationToken, token=serializer.validated_data['token'])

        if not token.is_expired:
            token.is_expired = True
            token.save()

            user = token.user
            user.is_active = True
            user.save()

            return Response({"message": "user activation successful"})
        else:
            return Response(
                {
                    'status': 'invalid token',
                    'message': "expired token"
                }, status=401)


class ResendActivationEmail(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = type('', (Serializer,),{'email': EmailField(required=True, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=serializer.validated_data['email'])

        if not user.is_active:
            user.send_activation_email()
            return Response({"message": "Activation email successfully sent"})
        else:
            return Response(
                {
                    'status': 'Invalid operation',
                    'message': "user is already activated"
                }, status=403)



