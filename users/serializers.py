from rest_framework import serializers

from django.conf.global_settings import EMAIL_HOST_USER

import requests, json


import members.models
import member_types.models
from .models import *


class UserInlineSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    member_type = serializers.PrimaryKeyRelatedField(many=False, queryset=member_types.models.MemberType.objects.all(), write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'member_type')

    def create(self, validated_data):
        member_type = validated_data.pop('member_type')
        created_user = User.objects.create_user(**validated_data)
        member = members.models.Member(user=created_user, member_type=member_type)
        member.save()

        user_activation_token = ActivationToken.objects.create(
            user=created_user, token=get_random_string(length=6))
        user_activation_token.save()


        #send the token to the user
        subject, from_email, to = 'activation code', 'from@example.com', 'to@example.com'
        text_content = 'Welcome, the actication code for your account is %s' % (
            user_activation_token.token)
        html_content = '<p>The activation code is  <strong>%s</strong> message.</p>'%(user_activation_token.token)
        send_mail(subject,text_content,EMAIL_HOST_USER,[created_user.email],fail_silently=False)
        
        #register on mfs
        header = {"Authorization": "Bearer TestAPIKey"}
        payload = {
            "Request":{
                "mobile_number": created_user.phone_number,
                "customer_name": created_user.first_name + " " +created_user.last_name,
                "account_number": created_user.national_id,
                "customer_id_number": created_user.national_id,
                "registration_code": "7840",
                "email_address": created_user.email
            }
        }        


        r = requests.post("https://mobiloantest.mfs.co.ke/api/v1/whitelist/opt_in",
                  data=json.dumps(payload), headers=header)

        try:
            if(r.status_code == 200):
                response = r.json()
                if(response["Response"]['status_code'] == 200):
                    member.is_msf_active = True
                else:
                    member.is_msf_active = False
                member.save()
        except:
            raise("cannot creat MFS account")

        return created_user

class ActivationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationToken
