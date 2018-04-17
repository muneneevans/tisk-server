
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers

from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.conf.global_settings import EMAIL_HOST_USER

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


        #send the token to the user
        subject, from_email, to = 'activation code', 'from@example.com', 'to@example.com'
        text_content = 'Welcome, the actication code for your account is %s' % (
            user_activation_token.token)
        html_content = '<p>The activation code is  <strong>%s</strong> message.</p>'%(user_activation_token.token)
        # msg = EmailMultiAlternatives(
        #     subject, text_content, EMAIL_HOST_USER, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()


        send_mail(subject,text_content,EMAIL_HOST_USER,[created_user.email],fail_silently=False)
        
        return created_user


class ActivationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationToken


        



