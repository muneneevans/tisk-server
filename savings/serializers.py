from rest_framework.serializers import ModelSerializer
from django.db import transaction

from .models import *
from users.models import User


class DepositInlineSerializer(ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"


class UserDepositSerializer(ModelSerializer):
    user_deposit = DepositInlineSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  'phone_number', "user_deposit")
