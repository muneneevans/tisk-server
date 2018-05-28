import rest_framework.serializers

from member_types.models import MemberType
from member_types.serializers import MemberTypeInlineSerializer
from membership_categories.models import MembershipCategory


class MembershipCategorySerializer(rest_framework.serializers.ModelSerializer):
    member_types = MemberTypeInlineSerializer(source='membertype_set', many=True)
    class Meta:
        model = MembershipCategory
        fields = "__all__"