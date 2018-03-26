
from rest_framework import serializers
from django.db import transaction
from .models import *


class UserInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'phone_number', 'first_name', 'last_name')

    def create(self, validated_data):        
        created_user = User.objects.create_user(**validated_data)

        return created_user
