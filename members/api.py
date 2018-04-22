from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .serializers import *
from .models import *
from users.permissions import isOwner


class UserMembershipView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    queryset = User.objects.all()
    model = User
    serializer_class = UserMembershipSerializer
    lookup_field = 'email'
