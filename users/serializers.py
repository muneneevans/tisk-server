
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers

from .models import *
class UserInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'phone_number', 'first_name', 'last_name', 'national_id')

    def create(self, validated_data):
        created_user = User.objects.create_user(**validated_data)

        user_activation_token = ActivationToken.objects.create(
            user=created_user, token=get_random_string(length=6))
        
        user_activation_token.save()
        return created_user
