from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *
from users.models import User


class UserDepositsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    model = User    
    serializer_class = UserDepositSerializer
    lookup_field = 'email'


class CreateDepositView(CreateAPIView):
    permission_classes = [AllowAny, ]
    # permission_classes = [IsAuthenticated, ]
    model = Deposit
    serializer_class = CreateDepositSerializer
