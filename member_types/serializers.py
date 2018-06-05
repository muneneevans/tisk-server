from rest_framework.serializers import ModelSerializer

from .models import *


class MemberTypeInlineSerializer(ModelSerializer):
    class Meta:
        model = MemberType
        fields = "__all__"


class MemberTypeSerializer(MemberTypeInlineSerializer):
    from membership_categories.serializers import MembershipCategoryInlineSerializer
    membership_category = MembershipCategoryInlineSerializer()