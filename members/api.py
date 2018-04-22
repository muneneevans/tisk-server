import uuid

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.fields import EmailField, CharField
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from members import permissions
from .serializers import *

class ActivateMFS(GenericAPIView):
    permission_classes = (permissions.IsMFSInactive,)

    def get(self, request, **kwargs):
        member = request.user.member
        member.is_msf_active = True
        member.msf_account = uuid.uuid4()
        member.save()
        return JsonResponse({"message": "MFS account successfully activated"})

    def post(self, request, **kwargs):
        return self.get(request, **kwargs)