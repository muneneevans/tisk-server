from django.db import transaction
from rest_framework import serializers
from .models import *
from users.models import *
class MemberInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('member_type', 'is_msf_active', 'msf_account')


class UserMembershipSerializer(serializers.ModelSerializer):
    user_member = MemberInlineSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'phone_number',
                  'first_name', 'last_name', 'national_id', 'user_member')
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
