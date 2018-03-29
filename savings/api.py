from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *
from users.models import User


class UserDepositsView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    model = User
    queryset = User.objects.all()
    serializer_class = UserDepositSerializer

    def get_queryset(self):
        queryset = super(UserDepositsView, self).get_queryset()
        return queryset.filter(email=self.kwargs.get('email'))


class CreateDepositView(CreateAPIView):
    permission_classes = [AllowAny, ]
    # permission_classes = [IsAuthenticated, ]
    model = Deposit
    serializer_class = CreateDepositSerializer
