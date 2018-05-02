import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.fields import EmailField, CharField
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from users.permissions import isOwner
from members import permissions
from members.serializers import *
from members.models import *


class UserMembershipView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    queryset = User.objects.all()
    model = User
    serializer_class = UserMembershipSerializer
    lookup_field = 'email'


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
