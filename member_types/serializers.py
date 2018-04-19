from rest_framework.serializers import ModelSerializer

from .models import *


class MemberTypeInlineSerializer(ModelSerializer):
    class Meta:
        model = MemberType
        fields = "__all__"