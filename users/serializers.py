
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
        fields = ('email', 'password', 'phone_number',
                  'first_name', 'last_name', 'national_id')

    def create(self, validated_data):
        created_user = User.objects.create_user(**validated_data)

        user_activation_token = ActivationToken.objects.create(
            user=created_user, token=get_random_string(length=6))

        user_activation_token.save()
        return created_user


class ActivationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationToken


class ActivateTokenSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer()
    class Meta:
        model = ActivationToken
        fields = ("is_expired","user")

    def update(self, instance, validated_data):
        import pdb
        pdb.set_trace()
        instance.token = validated_data.get('token', instance.token)
        # instance.email = validated_data.get('email', instance.email)
        # instance.content = validated_data.get('content', instance.content)
        # instance.created = validated_data.get('created', instance.created)
        return instance
        



